package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	if len(os.Args) < 4 {
		fmt.Println("Please provide ServiceName, PersonID, and LastName as arguments.")
		return
	}

	serviceName := os.Args[1]
	personID := os.Args[2]
	lastName := os.Args[3]

	for {
		fmt.Printf("[%s] Person ID: %s, Last Name: %s\n", serviceName, personID, lastName)
		time.Sleep(10 * time.Second)

	}
}
