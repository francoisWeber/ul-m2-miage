# Vespa Configuration

This directory contains configuration files for Vespa search engine.

## Quick Start

Vespa configurations will be automatically loaded when the container starts.

## Example Application Package

To create a Vespa application for beer search:

1. Create an application package structure
2. Define schemas for your data
3. Deploy the application to Vespa

### Example Schema

```xml
schema beer {
    document beer {
        field beer_id type int {
            indexing: summary | attribute
        }
        field name type string {
            indexing: summary | index
        }
        field description type string {
            indexing: summary | index
        }
        field abv type float {
            indexing: summary | attribute
        }
    }
    
    fieldset default {
        fields: name, description
    }
}
```

## Resources

- [Vespa Documentation](https://docs.vespa.ai/)
- [Vespa Sample Applications](https://github.com/vespa-engine/sample-apps)

