-- Keep a log of any SQL queries you execute as you solve the mystery.

--See all tables in data
.schema

-- 1. View data in Crime reports table for the date of the robbery
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28 AND year = 2023;

--crime scene report, 3 witnesses at bakery mention duck being stolen in interveiws
--2. view what witnesses said in interveiws regarding theft

SELECT * FROM interviews WHERE day = 28 AND month = 7 AND year = 2023;

--From the interveiws we know that the thief:
--drove away in a car from the bakery parking lot within 10 minutes of theft
--earlier in the morning withdrew from an ATM of Leggett Street and Eugene recognised them
--the thief called someone as they left the bakery for less than 1 minute
--thief will take earliest flight out of fiftyville tomorrow 29/07/2023, the receiver of the call purchased the ticket (accomplice)

--3. Examine security footage
SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2023;

--4. Examine ATM data, all the names, passports and phone numbers of people who used the atm on that day
SELECT name, passport_number, license_plate, phone_number FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
JOIN atm_transactions on bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2023 AND day = 28 AND month = 7 AND atm_location = 'Leggett Street';
-- This narrows it down to 9 people

--5. Compare license plates to bakery security log

SELECT DISTINCT license_plate FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND year = 2023
AND license_plate IN (
SELECT license_plate FROM people
JOIN bank_accounts on people.id = bank_accounts.person_id
JOIN atm_transactions on bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2023 AND day = 28 AND month = 7 AND atm_location = 'Leggett Street'
);

--This narrows it down to 5 number plates, feed this back into people to find names and everything else

SELECT * FROM people
WHERE license_plate IN ('L93JTIZ', '94KL13X', '1106N58', '322W7JE', '4328GD8');

--This gives the result below
-- |   id   |  name  |  phone_number  | passport_number | license_plate |
--+--------+--------+----------------+-----------------+---------------+
--| 396669 | Iman   | (829) 555-5269 | 7049073643      | L93JTIZ       |
--| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
--| 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
--| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       |
--| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X


--6.) Analyze call data of less than one minute that was with numbers in above table
SELECT * FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60 AND caller IN (
SELECT phone_number FROM people
WHERE license_plate IN ('L93JTIZ', '94KL13X', '1106N58', '322W7JE', '4328GD8')
);
-- This narrows it down to 3 numbers, feed this back into people to get all details

SELECT * FROM people
WHERE phone_number IN
(
SELECT caller FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60 AND caller IN
(
SELECT phone_number FROM people
WHERE license_plate IN ('L93JTIZ', '94KL13X', '1106N58', '322W7JE', '4328GD8')
)
);
--Assuming we don't know if the theif or accomplice started the call either are in this table
--+--------+--------+----------------+-----------------+---------------+
--|   id   |  name  |  phone_number  | passport_number | license_plate |
--+--------+--------+----------------+-----------------+---------------+
--| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
--| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       |
--| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
--+--------+--------+----------------+-----------------+---------------+

SELECT * FROM people
WHERE phone_number IN
(
SELECT receiver FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60 AND caller IN
(
SELECT phone_number FROM people
WHERE license_plate IN ('L93JTIZ', '94KL13X', '1106N58', '322W7JE', '4328GD8')
)
);
--Or this one, the theif and there accomplice is one person from either table
--+--------+--------+----------------+-----------------+---------------+
--|   id   |  name  |  phone_number  | passport_number | license_plate |
--+--------+--------+----------------+-----------------+---------------+
--| 250277 | James  | (676) 555-6554 | 2438825627      | Q13SVG6       |
--| 847116 | Philip | (725) 555-3243 | 3391710505      | GW362R6       |
--| 864400 | Robin  | (375) 555-8161 | NULL            | 4V16VO0       |
--+--------+--------+----------------+-----------------+---------------+

--7. Analyse airport data, find earliest flight on 29/07/2023

SELECT * FROM flights WHERE day = 29 AND month = 7 AND year = 2023 ORDER BY hour LIMIT 1;

--confrim flight number is 36

SELECT passport_number FROM passengers
WHERE flight_id = 36 AND passport_number IN
(
SELECT passport_number FROM people
WHERE phone_number IN
(
SELECT caller FROM phone_calls
WHERE day = 28 AND month = 7 AND year = 2023 AND duration < 60 AND caller IN
(
SELECT phone_number FROM people
WHERE license_plate IN ('L93JTIZ', '94KL13X', '1106N58', '322W7JE', '4328GD8')
)
)
);

--Narrowed it down to
-- 5773159633 Bruce
-- 1988161715 Taylor

--See full details for these two two numbers

SELECT * FROM people WHERE passport_number IN (5773159633, 1988161715)

-- Bruce and Robin OR
-- Taylor and James

-- Crime report states that the thief got into the car and drove away within 10 minutes of the robbery which happened at 10.15am, but Taylor's car exited the bakery at 10.35 which is 20 minutes.
-- Bruce's car left 3 minutes after the robbery 10.18 so bruce is the thief who called Robin who is thus the accomplice

-- Find city they went to 
SELECT city FROM airports
WHERE id = (SELECT destination_airport_id FROM  flights WHERE id = 36);




