# Given = where you start. When = what you do. Then = what you expect.
# And repeats the previous kind of step.
Feature: Home page

  Background:
    Given the home page is open
    Then the main heading is visible
    And Start Practicing is visible
    And Browse Interview Questions is visible

  @smoke
  Scenario: Start Practicing opens the sandbox list
    When the user clicks Start Practicing
    Then the Practice Sites heading is visible