Feature: Site menu

  @smoke
  Scenario: The menu opens Practice Sites
    Given the home page is open
    When the user opens Practice Sites from the menu
    Then the Practice Sites heading is visible

  @smoke
  Scenario: The menu opens Interview Prep
    Given the home page is open
    When the user opens Interview Prep from the menu
    Then the Interview library heading is visible
    And the interview search box is visible

  @smoke
  Scenario: The menu opens About
    Given the home page is open
    When the user opens About from the menu
    Then the About heading is visible

  @smoke
  Scenario: The menu opens Contact
    Given the home page is open
    When the user opens Contact from the menu
    Then the Contact heading is visible

  @smoke
  Scenario: The logo returns home
    Given the contact page is open
    When the user clicks the logo
    Then the main heading is visible
