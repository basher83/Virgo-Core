# Firecrawl SDK Research Tool

A powerful command-line tool for performing web research using Firecrawl's search and scrape APIs. Designed to find high-quality technical examples, documentation, and code repositories by combining web search, content scraping, quality filtering, and result ranking.

## Features

- **Category-Focused Search**: Filter searches by GitHub repositories, research papers, or PDFs
- **Combined Search+Scrape**: Efficiently combines search and scraping in a single API call
- **Quality Filtering**: Automatically filters and ranks results by quality indicators
- **Retry Logic**: Built-in exponential backoff for handling transient API failures
- **Rich Output**: Generates comprehensive markdown research documents with quality scores

## Quick Start

### Prerequisites

- Python 3.11 or higher
- `uv` package manager (for running the script)
- Firecrawl API key ([Get one here](https://firecrawl.dev/))

### Installation

1. Set your Firecrawl API key:
```bash
export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"
```

2. Make the script executable (if needed):
```bash
chmod +x scripts/firecrawl_sdk_research.py
```

The script uses `uv` to manage dependencies automatically - no manual installation required!

### Basic Usage

Search for technical examples on GitHub:
```bash
./scripts/firecrawl_sdk_research.py "ansible proxmox ceph" --category github
```

Search research papers:
```bash
./scripts/firecrawl_sdk_research.py "machine learning transformers" --category research
```

Search PDFs:
```bash
./scripts/firecrawl_sdk_research.py "kubernetes architecture" --category pdf
```

## Usage Examples

### Finding Code Examples

Search GitHub for Ansible Proxmox Ceph management examples:
```bash
./scripts/firecrawl_sdk_research.py "ansible proxmox ceph" \
  --category github \
  --limit 10 \
  --output ai_docs/ansible-proxmox-ceph.md
```

### Research Papers

Find academic papers on a topic:
```bash
./scripts/firecrawl_sdk_research.py "neural network optimization" \
  --category research \
  --limit 15 \
  --output research/papers.md
```

### Multiple Categories

Search across GitHub and research sources:
```bash
./scripts/firecrawl_sdk_research.py "distributed systems consensus" \
  --categories github,research \
  --limit 20
```

### Custom Output Location

Save results to a specific file:
```bash
./scripts/firecrawl_sdk_research.py "terraform aws eks" \
  --category github \
  --output docs/terraform-eks-examples.md
```

## Command-Line Options

```text
Usage: firecrawl_sdk_research.py [OPTIONS] QUERY

Arguments:
  QUERY                    Search query for research [required]

Options:
  --limit, -l INTEGER      Number of search results to scrape [default: 10]
  --output, -o TEXT        Output markdown file path [default: ai_docs/research.md]
  --category, -c TEXT      Search category: GitHub, research, or pdf
  --categories TEXT        Comma-separated list of categories: GitHub,research,pdf
  --help                   Show this message and exit
```

### Options Explained

- **`QUERY`** (required): Your search query string
- **`--limit, -l`**: Maximum number of results to scrape (default: 10)
- **`--output, -o`**: Path to output markdown file (default: `ai_docs/research.md`)
- **`--category, -c`**: Single category filter (GitHub, research, or pdf)
- **`--categories`**: Comma-separated list of categories (e.g., `GitHub,research`)

## Output Format

The script generates a comprehensive markdown document with the following sections:

### 1. Metadata Section
- Query string
- Generation timestamp
- Categories used
- Search and scrape statistics

### 2. Summary Section
- Total results found
- Successfully scraped pages
- High-quality source count

### 3. Sources Section
- Numbered list of all sources
- Quality indicators:
  - ⭐ = High quality (score ≥ 10)
  - ✓ = Medium quality (score ≥ 5)
- Domain information
- Quality scores

### 4. Content Section
- Full scraped content for each source
- Source URLs and metadata
- Quality scores and domain information

## Quality Scoring

Results are automatically scored and ranked based on:

- **Domain Quality** (+10 points): Prioritizes trusted domains:
  - `github.com`, `docs.github.com`
  - `docs.ansible.com`, `ansible.com`
  - `pve.proxmox.com`, `proxmox.com`
  - `docs.ceph.com`

- **GitHub Repository** (+5 points): Additional boost for GitHub repos

- **Content Length**:
  - +3 points for content > 2000 characters
  - +1 point for content > 1000 characters

- **Code Blocks** (+2 points): Presence of code blocks indicates technical content

Results are filtered to exclude:
- Content shorter than 500 characters
- Error pages (404, access denied, etc.)
- Low-quality domains

## How It Works

1. **Search**: Uses Firecrawl's search API with optional category filtering
2. **Scrape**: Automatically scrapes content from search results (combined operation)
3. **Filter**: Filters results by quality indicators and content length
4. **Rank**: Sorts results by quality score (highest first)
5. **Combine**: Generates a comprehensive markdown research document

## Error Handling

The script includes robust error handling:

- **Retry Logic**: Automatic retry with exponential backoff (3 attempts)
- **Graceful Failures**: Failed scrapes are logged but don't stop the process
- **Fallback**: If combined search+scrape fails, falls back to separate operations
- **Quality Fallback**: If all results are filtered out, saves unfiltered results with a warning

## API Costs

Firecrawl pricing considerations:

- **Search without scraping**: 2 credits per 10 search results
- **Search with scraping**: Standard scraping costs apply (no additional search charge)
- **PDF parsing**: 1 credit per PDF page (can be expensive for multi-page PDFs)

To minimize costs:
- Use `--limit` to control the number of results
- Avoid PDF category unless specifically needed
- The script uses efficient combined search+scrape operations

## Troubleshooting

### "FIRECRAWL_API_KEY environment variable not set"

Set your API key:
```bash
export FIRECRAWL_API_KEY="fc-your-api-key"
```

### "No search results found"

- Check your query spelling
- Try a broader search term
- Verify your API key is valid
- Check Firecrawl service status

### "Failed to scrape any content"

- Some URLs may be inaccessible or require authentication
- The script will continue with successfully scraped results
- Check the console output for specific error messages

### Low-quality results

- Use `--category GitHub` for code examples
- Increase `--limit` to get more results
- Quality filtering may be too strict - check the output for unfiltered results

## Future Enhancements

Potential improvements and features that could be added:

### Search Enhancements
- [ ] **Query Expansion**: Automatically expand queries with synonyms or related terms
- [ ] **Time-Based Filtering**: Add `--since` option to filter results by date
- [ ] **Language Filtering**: Support `--lang` option for specific languages
- [ ] **Site-Specific Search**: Add `--site` option to search within specific domains

### Quality Improvements
- [ ] **Custom Quality Domains**: Allow users to specify custom quality domains via config file
- [ ] **Star Count Integration**: For GitHub repos, fetch and use star counts in quality scoring
- [ ] **Last Updated Date**: Prioritize recently updated repositories
- [ ] **Readme Quality**: Analyze README quality for GitHub repos
- [ ] **License Detection**: Filter by open-source licenses

### Output Enhancements
- [ ] **Multiple Formats**: Support JSON, HTML, or CSV output formats
- [ ] **Summary Generation**: Use LLM to generate executive summaries
- [ ] **Code Extraction**: Extract and highlight code snippets separately
- [ ] **Link Validation**: Check and report broken links
- [ ] **Deduplication**: Detect and merge duplicate content

### Performance & Features
- [ ] **Caching**: Cache search results to avoid redundant API calls
- [ ] **Incremental Updates**: Append new results to existing research files
- [ ] **Parallel Processing**: Increase concurrency for faster scraping
- [ ] **Progress Bar**: Add progress indicators for long-running searches
- [ ] **Resume Support**: Resume interrupted searches from checkpoint

### Integration
- [ ] **CI/CD Integration**: GitHub Actions workflow for automated research
- [ ] **Notion Export**: Direct export to Notion databases
- [ ] **Obsidian Integration**: Generate Obsidian-compatible markdown with backlinks
- [ ] **Webhook Support**: Send results to webhooks for automation

### Advanced Filtering
- [ ] **Content Type Filtering**: Filter by file types (YAML, Python, etc.)
- [ ] **Repository Size**: Filter by repository size or activity level
- [ ] **Author Filtering**: Filter by GitHub username or organization
- [ ] **Topic Tags**: Filter GitHub repos by topics/tags

### Analysis Features
- [ ] **Trend Analysis**: Track how search results change over time
- [ ] **Comparison Mode**: Compare results from different queries
- [ ] **Dependency Analysis**: Extract and analyze dependencies from code
- [ ] **Best Practices Extraction**: Identify common patterns across results

## Contributing

Contributions welcome! Areas for improvement:

1. Additional quality scoring heuristics
2. Support for more Firecrawl API features
3. Output format enhancements
4. Performance optimizations
5. Documentation improvements

## License

See the repository LICENSE file for details.

## Related Tools

- [Firecrawl Documentation](https://docs.firecrawl.dev/)
- [Firecrawl Python SDK](https://docs.firecrawl.dev/sdks/python)
- [Firecrawl API Reference](https://docs.firecrawl.dev/api-reference/v2-introduction)

## Support

For issues or questions:
1. Check the [Firecrawl documentation](https://docs.firecrawl.dev/)
2. Review the troubleshooting section above
3. Open an issue in the repository
