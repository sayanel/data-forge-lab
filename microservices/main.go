package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"strconv"
	"sync"
	"syscall"
	"time"
)

// Person represents the structure of the JSON response
type Person struct {
	Address      string `json:"address"`
	DateOfBirth  string `json:"date_of_birth"`
	Email        string `json:"email"`
	FirstName    string `json:"first_name"`
	Gender       *string `json:"gender"`
	LastName     string `json:"last_name"`
	PersonID     string `json:"person_id"`
	PhoneNumber  string `json:"phone_number"`
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("Please provide the number of persons as an argument.")
	}

	n, err := strconv.Atoi(os.Args[1])
	if err != nil {
		log.Fatalf("Invalid number of persons: %v", err)
	}

	// URL of the REST API
	url := "http://localhost:5000/api/persons"

	// Make the HTTP GET request
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Failed to make request: %v", err)
	}
	defer resp.Body.Close()

	// Check if the response status is OK
	if resp.StatusCode != http.StatusOK {
		log.Fatalf("Received non-200 response code: %d", resp.StatusCode)
	}

	// Read the response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Failed to read response body: %v", err)
	}

	// Unmarshal the JSON response into a slice of Person structs
	var persons []Person
	err = json.Unmarshal(body, &persons)
	if err != nil {
		log.Fatalf("Failed to unmarshal JSON: %v", err)
	}

	// Ensure we have enough persons
	if n > len(persons) {
		log.Fatalf("Not enough persons in the response. Requested: %d, Available: %d", n, len(persons))
	}

	var wg sync.WaitGroup
	commands := make([]*exec.Cmd, n)
	microserviceNames := make([]string, n)

	// Create and run microservices
	for i := 0; i < n; i++ {
		person := persons[i]
		microserviceName := fmt.Sprintf("microservice-%d-%s", i+1, person.FirstName)
		cmd := runMicroservice(microserviceName, person.PersonID, person.LastName)
		commands[i] = cmd
		microserviceNames[i] = microserviceName
		log.Printf("[%s] Microservice created successfully with PID %d", microserviceName, cmd.Process.Pid)
		wg.Add(1)
		go func(name string, cmd *exec.Cmd) {
			defer wg.Done()
			// Wait for the process to exit
			err := cmd.Wait()
			if err != nil {
				log.Printf("[%s] Microservice exited with error: %v", name, err)
			}
		}(microserviceName, cmd)
	}

	// Wait for interrupt signal to gracefully shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

    // Shutdown all microservices
    for i, cmd  := range commands {
        if cmd.Process != nil {
            // Send a termination signal to the process
            err := cmd.Process.Signal(syscall.SIGTERM)
            if err != nil {
                log.Printf("[%s] Failed to terminate process with PID %d: %v", microserviceNames[i], cmd.Process.Pid, err)
            } else {
                // Give the process some time to shut down gracefully
                time.Sleep(2 * time.Second)
                // Forcefully kill the process if it didn't terminate
                err := cmd.Process.Kill()
                if err != nil {
                    log.Printf("[%s] Failed to kill process with PID %d: %v", microserviceNames[i], cmd.Process.Pid, err)
                }
            }
        }
    }

	wg.Wait()
	fmt.Println("All microservices have been shut down.")
}

func runMicroservice(name, personID, lastName string) *exec.Cmd {
	// Run the microservice template directly in the same terminal
	cmd := exec.Command("go", "run", "microservice_template.go", name, personID, lastName)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Start()
	if err != nil {
		log.Fatalf("[%s] Failed to start microservice: %v", name, err)
	}
	return cmd
}
