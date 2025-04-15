import { faker } from '@faker-js/faker';

export function generateRandomPerson() {
    return {
        person_id: faker.string.uuid(),
        first_name: faker.person.firstName(),
        last_name: faker.person.lastName(),
        date_of_birth: faker.date.birthdate().toISOString().split('T')[0],
        email: faker.internet.email(),
        phone_number: faker.phone.number(),
        address: faker.address.streetAddress(),
        gender: faker.name.sex(),
        notification_preferences: {
            email: faker.datatype.boolean(),
            sms: faker.datatype.boolean(),
        },
        language_preference: faker.locale,
        creation_date: faker.date.recent().toISOString().split('T')[0],
        last_updated: faker.date.recent().toISOString().split('T')[0],
    };
}
