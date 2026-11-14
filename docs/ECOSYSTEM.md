# Pain001 ecosystem

| Repository | Purpose | Quality contract |
| --- | --- | --- |
| `pain001` | Core library, CLI and REST service | typed API, schema/rulebook validation, 100% line and branch coverage |
| `pain001-mcp` | Read-only tools for AI agents | local stdio transport, no payment submission |
| `pain001-lsp` | Editor diagnostics and completion | shared validation semantics |
| `pain001-loader-mt101` | SWIFT MT101 ingestion | explicit field mapping and migration tests |
| `pain001-loader-xlsx` | Excel ingestion | numeric-account safety guard |
| `pain001-mockbank` | Synthetic SFTP pain.001 to pain.002 integration-test service | container image, synthetic data only |
| `pain001-plugin-template` | Cookiecutter scaffold for loader plugins | generated project passes its own gate in CI |
| `pain001-fast` | Experimental native validation helpers | source and wheels on GitHub releases |
| `pain001-sdk-go` | Go client for the REST API | Go 1.26, standard library only, `context.Context`; core's conformance kit run against a live `pain001 serve` in CI |
| `pain001-sdk-java` | Java client for the REST API | Java 17, Jackson databind; core's conformance kit run against a live `pain001 serve` in CI |
| `pain001-sdk-rust` | Rust client for the REST API | Rust 1.85, blocking, serde; core's conformance kit run against a live `pain001 serve` in CI |
| `pain001-sdk-dotnet` | .NET client for the REST API | .NET 10, async/await, `CancellationToken`; core's conformance kit run against a live `pain001 serve` in CI |
| `pain001-sdk-cpp` | C++ client for the REST API | C++17, libcurl and nlohmann/json; core's conformance kit run against a live `pain001 serve` in CI |
| `pain001.github.io` | Documentation and browser demo | SSG build, WCAG 2.2 AAA, Lighthouse 100, signed releases |

Each repository owns its API, package, release notes, and security response.
This website links them into one user journey but does not replace their
package documentation.
