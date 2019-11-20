# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0]
### Changed
- Updated CSCC module to use RESTfly and comply with CSCC v1 APIs.
- Script updated to use the new Integrations UA format used in restfly && pytenable.

### Fixed
- All tests now pass.

### Removed
- Removed the unused iterator in CSCC module.
- Removed superflouous tests interacting with no longer existent code.

## [1.0.1]
### Added
- Script now sets the Identity and integration version in the UserAgent string

## [1.0.0]
### Added
- Initial Version

[1.1.0]: https://github.com/tenable/integration-cscc/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/tenable/integration-cscc/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/tenable/integration-cscc/compare/1.0.0...1.0.0