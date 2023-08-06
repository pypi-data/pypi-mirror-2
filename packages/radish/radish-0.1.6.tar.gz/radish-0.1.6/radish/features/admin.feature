Feature: Login
  In order to have unlimited powers
  As a system anonymous user
  I want to login in the system

  Scenario: Successful admin login
    Given I am not logged in
    When I navigate to the admin page
    And I fill the "username" field with "admin"
    And I fill the "password" field with "admin"
    And I click the "Log in" button
    Then I should see the administration panel

  