# Architecture Decision Record

| # | Decision | Reason |
|---|----------|--------|
| 1 | Split the game into core logic, persistence, and pygame UI layers | Makes the game testable and easier to extend. |
| 2 | Keep the original checkerboard + red food visual language | Preserves the identity of the original repo while improving polish. |
| 3 | Persist only high score in a local JSON file | Adds value without introducing unnecessary complexity. |
