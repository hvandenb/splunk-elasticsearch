# Splunk Search Command for Elasticsearch

This is a Splunk search command that allows you to query an Elasticsearch index and view the results within the Splunk GUI.

## Requirements

*   Splunk Enterprise 8.x or later.
*   Python 3.7 or later.
*   Access to an Elasticsearch cluster.

## Installation

1.  **Install Python Dependencies:**

    This command needs the `elasticsearch` and `splunk-sdk` Python libraries. You can install them using pip:
    ```bash
    pip install elasticsearch splunk-sdk
    ```

2.  **Install the Splunk App:**

    Copy the `search-elasticsearch` directory to your Splunk apps folder:
    ```bash
    cp -r search-elasticsearch $SPLUNK_HOME/etc/apps/
    ```
    Alternatively, you can package the `search-elasticsearch` directory as a `.spl` file and install it through the Splunk UI.

3.  **Restart Splunk:**

    After installing the app, you will need to restart your Splunk instance.

## Usage

You can now use the `esearch` command in your Splunk search bar.

**Basic Example:**
```
| esearch q="some text"
```
This will search for "some text" in the `message` field of all indices.

**Advanced Example:**
```
| esearch oldest=now-100d earliest=now q="some text" index=nagios* limit=1000 field=message
```

### Command Reference

*   `q`: The query string to send to Elasticsearch. (Required)
*   `index`: The Elasticsearch index to search. (Default: `*`)
*   `limit`: The maximum number of records to return. (Default: 100)
*   `fields`: The field to query in Elasticsearch. (Default: `message`)
*   `oldest`: The oldest time for the search range (e.g., `now-1d`). (Default: `now`)
*   `earliest`: The earliest time for the search range. (Default: `now-1d`)
