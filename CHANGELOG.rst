=========
Changelog
=========

Version 1.5.0 (2026-03-25)
===========================

- **Polars rewrite** -- replaced ``pandas`` + ``swifter`` with ``polars>=1.0``
- Drop-in replacement: CLI interface, TSV output, and split algorithm unchanged
- Vectorized common preprocessing pipeline
  (URL decode, HTML strip, unicode category filter, whitespace normalization)
- Binary search for train/dev/test split sizes -- O(log N) vs O(N)
- Speaker-based split via O(n) join instead of O(n²) per-speaker filtering
- Fixed multi-locale processing bug (``del df`` inside loop)
- Fixed test-split safety cap (was ``train_size``, now correctly ``test_size``)
- Added Polars DataFrames based test suite

  *PR:* `#134 <https://github.com/common-voice/CorporaCreator/pull/134>`_


Version 1.4.2 (2026-03-23)
===========================

- New ``corporacreator.resources`` module for cross-platform memory probing
  (Linux ``/proc``, macOS ``getrusage``, Windows ``psutil``)
- ``[RESOURCES]`` DEBUG-level logging at critical pipeline points -- enabled with ``-vv``
- Reworked log formatter with ``CC-PY`` tag and ``%(module)s`` for bundler integration
- Explicit ``__all__`` re-exports per PEP 484
- Bump version to 1.4.2

  *PR:* `#133 <https://github.com/common-voice/CorporaCreator/pull/133>`_

Version 1.4.1
=============

- Multiple RAM/CPU optimizations for large datasets
- Use ``category`` dtypes to reduce memory pressure
- Free large DataFrames after use with explicit ``del`` + ``gc.collect()``
- Pre-partition speakers once O(n) instead of scanning per iteration O(n^2)
- Overcome Pandas concat issue via list comprehension
- Update ``.gitignore``

  *PR:* `#132 <https://github.com/common-voice/CorporaCreator/pull/132>`_

Version 1.4.0
=============

- Migrate to ``pyproject.toml`` (PEP 621) -- modern packaging
- **Python 3.12+ now required**
- Replace deprecated ``pkg_resources`` with ``importlib.metadata``
- Updated dependencies: ``pandas>=2.0``, ``swifter>=1.0``
- Improved type hints and development tools (ruff, mypy)
- Updated README with development instructions

  *PR:* `#131 <https://github.com/common-voice/CorporaCreator/pull/131>`_

Version 1.3.0
=============

- FIX: Require ``pandas < 3.0`` and fix ``setup.cfg`` dash issue

  *PR:* `#130 <https://github.com/common-voice/CorporaCreator/pull/130>`_

Version 1.2.1
=============

- FIX: Add comma to list item in ``read_csv`` dtype specification

Version 1.2.0
=============

- Add ``sentence_id`` column support

Version 1.1.0
=============

- Add ``sentence_domain`` column support

Version 1.0.1
=============

- FIX: ``read_csv`` options updated for newer pandas

Version 1.0.0
=============

- Initial tagged release
- Train/dev/test splitting based on statistical sample size
- Language-independent sentence cleaning (HTML, URL-encoded, control chars, digits)
- Language-dependent preprocessor plugins (de, cy, ky)
- Speaker-aware deduplication maintaining user diversity
- Configurable duplicate sentence count (``-s`` flag)
- Per-locale corpus creation with ``--langs`` filter
- Add ``variant`` column (`#124 <https://github.com/common-voice/CorporaCreator/pull/124>`_)
- Add ``accents`` column (`#118 <https://github.com/common-voice/CorporaCreator/pull/118>`_)
