# Accounts come from .env via helper.users.get_user.
# "valid" is the demo pair published on the login page.
# "invalid" is a pair the site rejects.
Feature: Practice login

  @smoke
  Scenario: The demo account signs in
    Given the login page is open
    When the user signs in as "valid"
    Then the login success message contains "Login Successful"

  @smoke
  Scenario: A wrong password is rejected
    Given the login page is open
    When the user signs in as "invalid"
    Then the login error message contains "Invalid email id and password"
