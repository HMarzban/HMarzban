# Making docs.plus builds smaller and faster

In docs.plus v2.0.1, I worked on reducing the cost of building and shipping the application. The editor's visible behavior stayed the same; the work was in the build and runtime setup.

## The problem

The webapp and collaboration backend had different runtime needs, but their images carried tools and dependencies they did not use. The webapp inherited native build tools and a second JavaScript runtime. The backend included two copies of Next.js even though it does not render pages.

A production build also spent 125 seconds on a permissions command that took only 1.8 seconds on a Mac laptop. Measuring locally alone made that cost easy to miss.

## What changed

I separated the webapp's build tools from its runtime image, removed an unused dependency-install step, and made better use of dependency and framework build caches. The [Docker optimization commit](https://github.com/docs-plus/docs.plus/commit/a19fede6c36d504e03b93604799db717ebad8c61) records those changes and their measurements.

The wider release also reduced the backend's runtime dependency set, corrected test scheduling, and replaced a fixed shutdown delay with an event-driven check. These changes are recorded in the [project changelog](https://github.com/docs-plus/docs.plus/blob/v2.0.1/CHANGELOG.md).

## Recorded results

The [v2.0.1 release](https://github.com/docs-plus/docs.plus/releases/tag/v2.0.1) records these before-and-after measurements:

| Measurement | Before | After |
| --- | ---: | ---: |
| Webapp image | 727 MB | 332 MB |
| Backend image | 5.67 GB | 961 MB |
| Production build | 997 seconds | 683 seconds |
| Backend tests | 7.9 seconds | 3.1 seconds |
| Extension tests | 209 seconds | 88 seconds |
| Full local check | 290 seconds | 163 seconds |

These are the project's recorded release measurements, not a fresh benchmark or a claim that every machine will see the same result. The release identifies production measurements but does not publish a complete hardware/cache-controlled benchmark protocol; the full-local-check measurement describes a separate local workflow. Use the linked commit and release for the original context.

## Decisions and tradeoffs

- **Build dependencies belong in the build stage.** Keeping them out of the runtime image reduces what has to be shipped while preserving the tools needed to compile the application.
- **A backend should ship its own dependency set.** A monorepo is useful for development, but it does not mean every service needs every package at runtime.
- **Caches need explicit boundaries.** Dependency changes must invalidate the relevant install layer; application changes should not force unrelated work to repeat.
- **Measure where the work happens.** The permissions step was a small cost on my laptop and a large one on the production server.

The useful result was a faster feedback loop and less unnecessary work in each build. Future measurements should record the commit, runner resources, cache state, and repeated timings so changes can be compared on the same basis.

[Back to my profile](../README.md)
