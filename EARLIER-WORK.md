# Earlier work

These projects show some of the problems I've explored over time. Their READMEs describe their individual status; the older toolchains and unfinished features are part of that history.

## A small web framework and its tools

[Ned](https://github.com/HMarzban/ned) is a SPA router and component-library experiment. The related repositories form one project family:

- [ned-cli](https://github.com/HMarzban/ned-cli): scaffolding and project commands.
- [ned-seed](https://github.com/HMarzban/ned-seed): a starter application.
- [ned-shards-dashboard-lite](https://github.com/HMarzban/ned-shards-dashboard-lite): integration with the credited Shards Dashboard template.
- [tscw](https://github.com/HMarzban/tscw): TypeScript compilation and Webpack watching.

The interesting part is the design of the router, components, and development workflow. The source development branch is [base_modular](https://github.com/HMarzban/ned/tree/base_modular); the default branch also contains demo and bundled assets.

## Calendar and data tools

[pipe2time.ir](https://github.com/HMarzban/pipe2time.ir) turns calendar data into JSON and ICS. [pipe2badesaba.ir](https://github.com/HMarzban/pipe2badesaba.ir) explores a similar workflow in Go. [ganjoor-mongodb](https://github.com/HMarzban/ganjoor-mongodb) is a MySQL-to-MongoDB migration utility for the Ganjoor dataset.

These projects depend on source data and external services, so a generated file's year is not a promise that the upstream data was recently verified.

## Hardware and mobile

[MagicMirror](https://github.com/HMarzban/MagicMirror) combines a Raspberry Pi mirror, Electron desktop interface, Ionic mobile application, and experiments with device communication. It preserves an earlier prototype, including features that were never completed.

[react-native-first-try](https://github.com/HMarzban/react-native-first-try) is a small mobile learning project with a recorded demonstration.

## Backend experiments

[ts-xarboilerplate](https://github.com/HMarzban/ts-xarboilerplate) is the TypeScript continuation of [xarboilerplate](https://github.com/HMarzban/xarboilerplate). Both preserve API and database testing work. [express-ts-zod](https://github.com/HMarzban/express-ts-zod) is a smaller request-validation example; [wsgateway](https://github.com/HMarzban/wsgateway) explores clustered WebSocket communication.

I also worked on [q2m](https://github.com/unicornist/q2m), a query-to-MongoDB library developed with Babak Khorrami. Its package is named `q2ma`.

[Back to my profile](README.md)
