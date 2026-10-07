Feature: Site menu (data driven)

  @smoke
  Scenario Outline: The menu opens <link>
    Given the "Home" page is open
    When the user opens "<link>" from the menu
    Then the page heading reads "<heading>"
    And the address ends with "<path>"

    Examples:
      | link           | heading                    | path                     |
      | Practice Sites | Practice Sites             | /practice-page-selection |
      | Interview Prep | Interview Question Library | /interview               |
      | About          | About QA Practice          | /AboutPage               |
      | Contact        | Contact QA Practice        | /contact                 |

  @smoke
  Scenario Outline: The logo returns home from <start page>
    Given the "<start page>" page is open
    When the user clicks the logo
    Then the page heading reads "The Ultimate Automation Playground"
    And the address ends with "/"

    Examples:
      | start page     |
      | Practice Sites |
      | Interview Prep |
      | About          |
      | Contact        |
