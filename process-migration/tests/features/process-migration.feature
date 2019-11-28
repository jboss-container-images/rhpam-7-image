@rhpam-7/rhpam77-process-migration
Feature: RHPAM Process Migration tests

   Scenario: Test REST API is available and valid
     When container is ready
     Then check that page is served
         | property | value |
         | port     | 8080  |
         | path     | /rest/health/status |
         | expected_phrase | SUCCESS |
