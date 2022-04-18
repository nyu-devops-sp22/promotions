Feature: The promotions micro-service back-end
    As a eCommerce Manager
    I need a RESTful catalog service
    So that I can keep track of all the promotions

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


    # When I paste the "Id" field
    # And I press the "Retrieve" button
    # Then I should see "Happy" in the "Name" field
    # And I should see "Hippo" in the "Category" field
    # And I should see "False" in the "Available" dropdown
    # And I should see "Male" in the "Gender" dropdown
    # And I should see "2022-06-16" in the "Birthday" field