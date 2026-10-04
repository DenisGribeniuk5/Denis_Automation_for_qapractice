"""
The practice-sites index should link to every sandbox.
Add a new locator on PracticeSitesPage when the site adds a sandbox,
then add it to sandbox_links so this test covers it.
"""

from playwright.sync_api import expect


def test_each_sandbox_has_a_link(practice_sites):
    for link in practice_sites.sandbox_links:
        expect(link).to_be_visible()
