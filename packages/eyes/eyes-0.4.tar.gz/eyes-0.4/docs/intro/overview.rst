.. _intro-overview:

================
Eyes Overview
================

Eyes is a project to enable quick, simple, and API enabled monitoring and data collection. Eyes (in it's current form) takes advantage of nagios plugins and wraps them with a Django web framework instead of the Nagios framework - intended to make dynamically creating, updating, and processing of monitor points far easier than it exists today.

First and foremost, Eyes has been created to enable systems and infrastructure with a very high rate of change. Fundamentally, this means being API driven from the base and going up - enabling the creation, destruction, and update of monitors and data sources at an API level so they can be programmatically manipulated.

Eyes is also built to be a component in a larger system, processing information and doing its work asynchronously from other components in the system.

The core of eyes is a poll-based system, but the REST API design allows for passive consumption of monitoring  data as well (i.e. agent based mechanisms).

Project Philosophy:
-------------------

* Open and platform neutral APIs supporting a distributed system: REST/JSON
* Expectation that the system is distributed, and of potential failure in subsystems
* A platform neutral, web based interface for humans to easily consume the information from Eyes
* support for Chrome, Safari, Firefox, and IE
* Testing for verification built into the application function from the start
* unit testing and functional testing structures built into the development process
* Documentation for Eyes to be built alongside the code
* - How to install and use the product
* - APIs and example code for manipulating Eyes

Overall Monitoring Goals:
-------------------------

#. API level access to all elements and components of a monitoring system
#. Auditing - all actions and changes to the system audited and traceable
#. Delegated Access
#. Ability to have external verification that the system is functional
#. The capability to monitor and report, but not alert
#. de-duplication of alerts/message storms through dependency analysis
#. templates for monitors and monitor sets
#. grouping and reporting in multiple dimensions
#. event correlation and alert suppression using a system model and additional logic

Detailed Goals:
---------------

1. API level access to all elements of the monitors
 * attributes (such as associated CI, priority/impact if monitor is triggered, thresholds if set centrally)
 * api to deploy a given monitor across 1..N additional servers/CI’s (maybe services in some cases)
 * api to create all elements of a monitor from scratch programmatically so that we can generate monitors when we deploy applications
 * api to enable the removal of monitors on decommissioning of a server or service

2. Audit ability
 * be able to associate, list, and report on what monitors exist against which servers & services (by CI in a CMDB)
 * be able to verify the content that a monitor triggers includes desired minimal information
 * * CI data label/link/reference
 * * Priority/Impact data label
 * Any relevant Knowledge Base instructions or documents for people responding to a monitor alert
 * Given a monitor template or collection of monitors, I want to know all the nodes it has been deployed to.
 * I want to be able to run basic reporting against nodes, policies, alert types.

3. Delegated access
 * enable folks outside of the core monitoring administrators to create and set up monitors
 * a end user should be able
 * * to create a monitor
 * * test a monitor
 * * ask that the monitor be deployed against 1..N systems
 * * update that monitor with new critical attributes (links to wiki articles, priority and/or impact of incidents on a failure, associations for the monitor to other systems)
 * In order to do delegated access properly we need to provide a feedback loop to whomever will be using/creating/editing monitors.  The users need to be able to see their alert, see that it is correct or incorrect, and be able to get feedback without intervention.  ie.  They need to be able to debug and fix their own problems.
 * They also need to be prevented from taking down the monitoring infrastructure.

4. Ability to have external verification that system is functional
 * external verification that the monitoring system is functioning
 * agents on systems (if relevant), message passing, and generating ticketing
 * integration flow verification from multiple remote data centers to any central consoles/servicedesk

5. Operational but not alerting
 * monitor, but not generate events during operator or engineering invoked "shut up, I'm doing maintenance" time
 * API to toggle this per monitor or all monitors associated to a CI

6. Dedupe/spamming
 * rate limiting event creation to keep from spamming and shutting down queues in system
 * internal monitoring and queue reporting to show efficiency and effectiveness of the system

7. Templates:
 * engineering (non core monitoring administrators) create templates for groups of monitors that can be applied to servers or services
 * be able to assume system variables (IP / hostname) as I apply them to the next server
 * For instance I would want to create a standard set of “DB SAN Server monitors” that would monitor HBAs, SQL queues, etc that would be added in addition to standard server monitors.
 * Ideally a SQL server would get “Standard Pack” + “SAN pack” + “MSSQL Pack” of monitors

8. Grouping and Reporting
 * I want to be able to group and report on the monitors in multiple different dimensions
 * I specifically *don't* want the reporting of monitors tied to a single hierarchy
 * some examples:
 * * All SQL monitors
 * * All Windows server monitors
 * * All SAN Disk monitors
 * Be able to reporting on monitors disabled for X days/weeks/months

9. Event correlation with CMDB using
 * custom logic designed by system engineering
 * delegated authority to implement/set/update these pieces of logic
 * some API level mechanism to enable auditing/reporting of the logic components and what CI’s are associated with these monitors