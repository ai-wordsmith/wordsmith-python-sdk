# Wordsmith SDK for Python
## Intro to Wordsmith

[Wordsmith](http://wordsmith.automatedinsights.com) makes it easy to generate thousands of stories, reports, and articles
in the time it takes to write just one. Wordsmith is a natural language
generation tool that enables users to turn data into text using dynamic
templates. The platform is easy to learn, and powerful enough to make each piece
of content totally unique.

The Wordsmith API allows developers to generate new content using the Templates
created in the Wordsmith web app by users at your company. Developers can use
the API to send new data which will trigger the generation of new text content.
You have complete control over when you generate and use the content.

## Installation

You will need access to the ai-invent GitHub repo in order to install this
package. Once you have access, you can use `pip` to install as follows:
`pip install git+ssh://git@github.com/ai-invent/wordsmith-python-sdk.git`

## Basic Usage

To add Wordsmith to your Python project, use:

```python
from wordsmith import Wordsmith
```

Wordsmith projects and templates have corresponding objects in this SDK. Below is some sample code to help get started.

### List All Projects
```python
from wordsmith import Wordsmith

ws = Wordsmith('<your_api_key_here>')
for project in ws.projects:
  print(project.name)
```

### Find A Project by Slug
```python
from wordsmith import Wordsmith

ws = Wordsmith('<your_api_key_here>')
project = ws.project('<project_slug_here>')
```

### Find A Project by Name
```python
from wordsmith import Wordsmith

ws = Wordsmith('<your_api_key_here>')
# Be careful as this returns a list (since Wordsmith allows duplicate project names)
matches = ws.find_project('<project_name>')
```

### Generate Narrative
```python
from wordsmith import Wordsmith

ws = Wordsmith('<your_api_key_here>')
# Send your data as a dictionary of key, value pairs where key is the sluggified column name and value is the
# value the column should have. Tip: you can send everything as strings and Wordsmith will handle conversion to
# numeric values where necessary.
data = {
  'col_1' : 'val_1',
  'col_2' : 'val_2'
}
print(ws.project('<project_slug>').template('<template_slug>').generate_narrative(data).text)
```

### Batch Generate Narrative
For generating a small number of narratives, a loop will likely suffice. There may be times, however, that you
need to generate a large volume of narratives. For this, you can use the batch generate functionality built into
this SDK. Batch generation uses multi-threading to process requests in parallel and reduce the overall
processing time.
```python
from wordsmith import Wordsmith

ws = Wordsmith('<your_api_key_here>')
# Send your data as a list of dictionaries. Structure your dictionaries as detailed in the Generate Narrative
# section above.
data = [
  {
    'col_1' : 'val_1',
    'col_2' : 'val_2'
  },
  {
    'col_1' : 'val_3',
    'col_2' : 'val_4'
  },
  {
    'col_1' : 'val_5',
    'col_2' : 'val_6'
  }
]

# You can optionally specify the number of threads used to generate narratives and whether you want to have your
# batch fail on any error. Beware that setting the number of threads too high may result in lost narratives or
# errors. The default value is to use 8 threads. You can set these options using the following form:
# batch.pool_size = 10
# batch.break_on_error = True
batch = ws.project('<project_slug>').template('<template_slug>').batch_narrative(data)
batch.generate()

# Get the text from the returned Narrative objects
results_text = [narrative.text for narrative in batch.narratives where narrative is not None]

print(results_text)
```

## API Documentation

This is where you'll find info on classes, methods, and properties.

## Wordsmith Class

This is the base class used to connect to the Wordsmith API.

### Initialization

```python
Wordsmith(api_key, base_url=<base_url>, user_agent=<user_agent>)
```
*Parameters*

| Name       | Required | Format | Description                                             |
|------------|:--------:|--------|---------------------------------------------------------|
| API Key    | Yes      | String | The user's API key for the Wordsmith platform           |
| Base URL   | No       | String | The base URL used to make requests to the Wordsmith API |
| User Agent | No       | String | The user agent passed to the Wordsmith API              |

### Properties

| Name          | Call Format          | Format Returned         | Description                                                         |
|---------------|----------------------|-------------------------|---------------------------------------------------------------------|
| Projects      | `wordsmith.projects` | List of Project objects | A list of all the Python objects associated with the passed API key |
| Configuration | `wordsmith.config`   | Configuration object    | Configuration details used to connect to the Wordsmith API          |

### Methods

**wordsmith.project(project_slug)**

Return a Wordsmith project object by the project's slug or return `None` if the template does not exist within the project.

| Argument     | Required | Format |
|--------------|:--------:|--------|
| Project Slug | Yes      | String |

**project.find_project(project_name)**

Find a Wordsmith project object or objects by name. Returns an empty list if no matching projects are found.

| Argument     | Required | Format |
|--------------|:--------:|--------|
| Project Name | Yes      | String |

## Project Class

This class represents a single Wordsmith project.

### Initialization

```python
Project(project_name, project_slug, project_schema, templates, configuration)
```

*Parameters*

| Name           | Required | Format     | Description                                                                                              |
|----------------|:--------:|------------|----------------------------------------------------------------------------------------------------------|
| Project Name   | Yes      | String     | The name of the project                                                                                  |
| Project Slug   | Yes      | String     | The project's sluggified name                                                                            |
| Project Schema | Yes      | Dictionary | The schema, as a Python dictionary, from Wordsmith                                                       |
| Templates      | Yes      | List       | A list of dictionaries, each dictionary containing the name and slug of a template owned by this project |
| Configuration  | Yes      | Object     | A configuration object, typically set by the Wordsmith object                                            |

### Properties

| Name      | Call Format         | Format Returned          | Description                                    |
|-----------|---------------------|--------------------------|------------------------------------------------|
| Name      | `project.name`      | String                   | The name of the project                        |
| Slug      | `project.slug`      | String                   | The sluggified name of the project             |
| Schema    | `project.schema`    | Dictionary               | The project's schema as a dictionary           |
| Templates | `project.templates` | List of Template objects | The templates owned by this project, as a list |

### Methods

**project.template(template_slug)**

Return a Wordsmith template object by the template's slug or return `None` if the template does not exist within the project.

| Argument      | Required | Format |
|---------------|:--------:|--------|
| Template Slug | Yes      | String |

**project.find_template(template_name)**

Find a Wordsmith template object or objects by name. Returns an empty list if no matching templates are found.

| Argument      | Required | Format |
|---------------|:--------:|--------|
| Template Name | Yes      | String |

## Template Class

This class represents a single Wordsmith template.

### Initialization

```python
Template(project_slug, template_name, template_slug, configuration)
```

*Parameters*

| Name          | Required | Format     | Description                                                                                              |
|---------------|:--------:|------------|----------------------------------------------------------------------------------------------------------|
| Project Slug  | Yes      | String     | The name of the project                                                                                  |
| Template Name | Yes      | String     | The project's sluggified name                                                                            |
| Template Slug | Yes      | Dictionary | The schema, as a Python dictionary, from Wordsmith                                                       |
| Configuration | Yes      | Object     | A configuration object, typically set by the Wordsmith object                                            |

### Properties

| Name         | Call Format            | Format Returned          | Description                                     |
|--------------|------------------------|--------------------------|-------------------------------------------------|
| Project Slug | `template.project_slug | String                   | The slug of the parent project                  |
| Name         | `template.name`        | String                   | The name of the template                        |
| Slug         | `template.slug`        | String                   | The sluggified name of the template             |

### Methods

**template.generate_narrative(data)**

Pass `data` to Wordsmith and generate narrative. The response is returned as a Narrative object. The `data` passed to this
method should be in a dictionary where keys correspond to Wordsmith data variables and the values correspond to the value
that the data variable should hold.

| Argument | Required | Format     |
|----------|:--------:|------------|
| Data     | Yes      | Dictionary |

**project.batch_narrative(data)**

Generate a batch narrative object that can be used to generate large volumes of narrative using multi-threading. The `data`
passed to this method should be formatted as a list of dictionaries where each dictionary has keys that correspond to
Wordsmith data variables and values that correspond to the value that the data variable should hold. *NOTE*: The batch
narrative object does not automatically generate all narratives, you must run the `.generate()` method on this object in
order to begin the process of generating narratives.

| Argument | Required | Format               |
|----------|:--------:|----------------------|
| Data     | Yes      | List of Dictionaries |

## Narrative Class

This class represents a single Wordsmith narrative.

### Initialization

```python
Narrative(project_slug, template_slug, data, configuration)
```

*Parameters*

| Name          | Required | Format     | Description                                                     |
|---------------|:--------:|------------|-----------------------------------------------------------------|
| Project Slug  | Yes      | String     | The project's sluggified name                                   |
| Template Slug | Yes      | String     | The templates's sluggified name                                 |
| Data          | Yes      | Dictionary | Dictionary where keys = column names and values = column values |
| Configuration | Yes      | Object     | A configuration object, typically set by the Wordsmith object   |

### Properties

| Name          | Call Format               | Format Returned | Description                                    |
|---------------|---------------------------|-----------------|------------------------------------------------|
| Project Slug  | `narrative.project_slug`  | String          | Sluggified name of the parent project          |
| Template Slug | `narrative.template_slug` | String          | Sluggified name of the parent template         |
| Data          | `narrative.data`          | String          | Data passed to Wordsmith to generate narrative |
| Text          | `narrative.text`          | String          | Narrative returned from Wordsmith              |

## Batch Class

This class represents a batch of Wordsmith narratives.

### Initialization

```python
Batch(project_slug, template_name, data_list, configuration)
```

*Parameters*

| Name          | Required | Format               | Description                                                                                        |
|---------------|:--------:|----------------------|----------------------------------------------------------------------------------------------------|
| Project Slug  | Yes      | String               | The project's sluggified name                                                                      |
| Template Slug | Yes      | String               | The templates's sluggified name                                                                    |
| Data List     | Yes      | List of Dictionaries | List of dictionaries where each dictionary is structured per the rules used by the Narrative class |
| Configuration | Yes      | Object               | A configuration object, typically set by the Wordsmith object                                      |

### Properties

| Name           | Call Format            | Format Returned      | Description                                                                                                                                                 |
|----------------|------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Project Slug   | `batch.project_slug`   | String               | Sluggified name of the parent project                                                                                                                          |
| Template Slug  | `batch.template_slug`  | String               | Sluggified name of the parent template                                                                                                                         |
| Data List      | `batch.data_list`      | List of Dictionaries | List of data passed to Wordsmith to generate narratives                                                                                                        |
| Narratives     | `batch.narratives`     | List                 | List of narratives produced by Wordsmith. If `break_on_error == False`, any failed narratives will generate a `None` in this list.                             |
| Errors         | `batch.errors`         | List                 | List of any errors encountered in producing the batch when `break_on_error == False`.                                                                          |
| Break on Error | `batch.break_on_error` | Boolean              | Sets whether the batch process should break when encountering an error. By default, `break_on_error` is set to `False`.                                        |
| Pool Size      | `batch.pool_size`      | Integer              | Number of pool workers to use in the multi-threading proceess. Default value is 8. Be cautious as setting this value too high could result in lost narratives. |

### Methods

**batch.generate()**

Begin the process of generating the batch of narratives based on the list of data contained in `batch.data_list`. Depending on how many
entries are in `batch.data_list` this process could be quite lengthy. By default, any errors encountered in generating the batch will
be logged in `batch.errors` and represented as `None` in `batch.narratives`. You can force this method to break when it hits an error
by setting `batch.break_on_error = True`.

| Argument | Required | Format |
|----------|:--------:|--------|
| N/A      | N/A      | N/A    |

## Error Types

The Wordsmith library implements several custom error types.

### ProjectSlugError

An invalid `project_slug` was passed to `wordsmith.project(project_slug)`.

### TemplateSlugError

An invalid `template_slug` was passed to `project.template(template_slug)`.

### NarrativeGenerateError

Wordsmith reported an error when trying to generate narrative(s).

**Properties**

| Name             | Call Format              | Format Returned | Description                                                               |
|------------------|--------------------------|-----------------|---------------------------------------------------------------------------|
| HTTP Status Code | `error.http_status_code` | Integer         | The HTTP status code for the request (400, 404, e.g.).                    |
| HTTP Reason      | `error.http_reason`      | String          | The HTTP reason for the request ("Bad Request", "Not Found", e.g.).       |
| Data             | `error.data`             | Dictionary      | The data passed to Wordsmith with the original request.                   |
| Details          | `error.details`          | List            | List of the error details, if any, reported by Wordsmith for the request. |

## Running Tests

Make sure you have pytest installed in your current environment with `pip install -U pytest`. Then from the root of this directory,
run `python -m pytest`.
