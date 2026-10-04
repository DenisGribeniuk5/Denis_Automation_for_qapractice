Feature: Interview library

  @smoke
  Scenario: The search box keeps the query
    Given the interview page is open
    When the user searches the interview library
    Then the search box shows the typed query

  @smoke
  Scenario: The JavaScript checkbox filters questions
    Given the interview page is open
    When the user checks the JavaScript filter
    Then the JavaScript checkbox is selected
    And 21 JavaScript questions are listed
    And every visible question is about JavaScript
