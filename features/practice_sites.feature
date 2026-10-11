Feature: Practice sites

  @smoke
  Scenario: Each sandbox has a link
    Given the practice sites page is open
    Then every sandbox link is visible
