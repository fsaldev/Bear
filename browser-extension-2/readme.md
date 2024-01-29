# Chrome Extension for NEAR wallet created with React Typescript

## Description

Front end project for Homepage extension wallet. The Chrome Extension is implemented using React + Typescript. For managing data requests it uses React Query.

## Installation

- Run ```npm install```

## Scripts availables

-    ```npm start```: Run the dev enviroment building a ./dist file and run the changes watcher.
-    ```npm run build```: Run the build with the production enviroment.
-    ```npm run lint```: Run the ESLint to check for lint errors.

## Deploy on chrome

- Go to chrome://extensions/.
- At the top right, turn on Developer mode.
-  Click Load unpacked.
- Find and select the app extension /dist folder that was generated with webpack.
- Open a new tab in Chrome and then click Apps and then click the app or extension. Make sure it loads and works correctly.
- If you are runing with the watcher active, the changes will refresh after you close and open againg the extension popup screen.

### Troubleshoot problems with your app or extension using Chrome logs:

Remember that you can inspect the chrome extension popup, but you also have available the background console in the Extensions section.
