# The form is filled and checked. The scenario does not click
# "Open email draft", because that opens the mail app.
Feature: Contact form

  @smoke
  Scenario: The form accepts a message
    Given the contact page is open
    When the user fills the contact form
    Then the contact form shows the typed message
    And the send button is visible
