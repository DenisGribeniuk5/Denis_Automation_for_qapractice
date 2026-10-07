Feature: Home page (data driven)

  Background:
    Given the "Home" page is open

  @smoke
  Scenario Outline: The home page shows <text>
    Then the home page shows "<text>"

    Examples:
      | text                               |
      | The Ultimate Automation Playground |
      | Start Practicing                   |
      | Browse Interview Questions         |

  @smoke
  Scenario Outline: <button> opens <heading>
    When the user clicks the hero button "<button>"
    Then the page heading reads "<heading>"
    And the address ends with "<path>"

    Examples:
      | button                     | heading                    | path                     |
      | Start Practicing           | Practice Sites             | /practice-page-selection |
      | Browse Interview Questions | Interview Question Library | /interview               |
