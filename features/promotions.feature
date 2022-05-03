Feature: The promotions micro-service back-end
    As a eCommerce Manager
    I need a RESTful catalog service
    So that I can keep track of all the promotions

Background:
    Given the following promotions
        | name          | start_date              | end_date             | type       | value   | ongoing    | product_id |
        | BigDiscount   | 03-15-2020 00:00:00     | 08-15-2020 00:00:00  | VALUE      | 10.0    | False      | 20         |
        | SmallDisCount | 08-19-2021 00:00:00     | 10-19-2021 00:00:00  | PERCENTAGE | 0.3     | False      | 15         |
        | Another       | 01-05-2022 00:00:00     | 05-09-2022 00:00:00  | VALUE      | 20.0    | True       | 19         |

Scenario: The server is running
    When I visit the "Home Page"
    And I click service
    Then I should see "Promotion Demo RESTful Service" in the title

Scenario: Create a Promotion
    When I visit the "Home Page"
    And I click service
    And I set the "Name" to "Happy"
    And I set the "Start Date" to "01-01-2022 00:00:00"
    And I set the "End Date" to "02-01-2022 00:00:00"
    And I set the "Value" to "1.0"
    And I set the "Product ID" to "1"
    And I select "False" in the "Ongoing" dropdown
    And I select "Value" in the "Type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Start Date" field should be empty
    And the "End Date" field should be empty
    And the "Value" field should be empty
    And the "Product ID" field should be empty
    And the "Type" field should be empty
    And the "Ongoing" field should be empty

Scenario: Delete a Promotion
    When I visit the "Home Page"
    And I click service
    And I set the "Name" to "Sales"
    And I set the "Start Date" to "01-05-2022 00:00:00"
    And I set the "End Date" to "02-19-2022 00:00:00"
    And I set the "Value" to "100.0"
    And I set the "Product ID" to "199"
    And I select "False" in the "Ongoing" dropdown
    And I select "Value" in the "Type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Delete" button
    Then I should see the message "promotion has been Deleted!"
    And the "ID" field should be empty
    When I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button 
    Then the "ID" field should be empty
    And the "Name" field should be empty
    And the "Start Date" field should be empty
    And the "End Date" field should be empty
    And the "Value" field should be empty
    And the "Product ID" field should be empty
    And the "Type" field should be empty
    And the "Ongoing" field should be empty

Scenario: Retrieve a Promotion
    When I visit the "Home Page"
    And I click service
    And I set the "Name" to "Sales"
    And I set the "Start Date" to "01-05-2022 00:00:00"
    And I set the "End Date" to "02-19-2022 00:00:00"
    And I set the "Value" to "100.0"
    And I set the "Product ID" to "199"
    And I select "False" in the "Ongoing" dropdown
    And I select "Value" in the "Type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Sales" in the "Name" field
    And I should see "01-05-2022 00:00:00" in the "Start Date" field
    And I should see "02-19-2022 00:00:00" in the "End Date" field
    And I should see "199" in the "Product ID" field
    And I should see "Value" in the "Type" dropdown
    And I should see "False" in the "Ongoing" dropdown
    And I should see "100" in the "Value" field
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Delete" button
    Then I should see the message "promotion has been Deleted!"
    And the "ID" field should be empty
    When I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button 
    Then I should not see the message "Success"

Scenario: Update a Promotion
    When I visit the "Home Page"
    And I click service
    And I set the "Name" to "BigDiscount"
    And I press the "Search" button
    Then I should see "BigDiscount" in the "Name" field
    And I should see "03-15-2020 00:00:00" in the "Start Date" field
    And I should see "08-15-2020 00:00:00" in the "End Date" field
    And I should see "20" in the "Product ID" field
    And I should see "Value" in the "Type" dropdown
    And I should see "False" in the "Ongoing" dropdown
    And I should see "10" in the "Value" field
    When I change "Name" to "BiggestDiscount"
    And I change "Start Date" to "03-20-2020 00:00:00"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "BiggestDiscount" in the "Name" field
    And I should see "03-20-2020 00:00:00" in the "Start Date" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "BiggestDiscount" in the results
    And I should not see "BigDiscount" in the results

Scenario: Invalidate a Promotion
    When I visit the "Home Page"
    And I click service
    And I set the "Name" to "SmallDiscount"
    And I set the "Start Date" to "01-09-2022 00:00:00"
    And I set the "End Date" to "03-29-2022 00:00:00"
    And I set the "Value" to "200.0"
    And I set the "Product ID" to "399"
    And I select "True" in the "Ongoing" dropdown
    And I select "Value" in the "Type" dropdown
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "SmallDiscount" in the "Name" field
    And I should see "True" in the "Ongoing" dropdown
    When I press the "Clear" button
    And I paste the "ID" field
    And I press the "Invalidate" button
    Then I should see the message "promotion has been Invalidated!"
    And the "ID" field should be empty
    When I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button 
    Then I should see "SmallDiscount" in the "Name" field
    And I should see "False" in the "Ongoing" dropdown
