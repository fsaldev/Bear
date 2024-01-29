import { result } from 'lodash';
import { css } from 'styled-components';
import WebSocket from 'ws';
declare const chrome: any;

console.log("Hello from content script! 2");

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

async function clickButtonByXpath(x_path: any) {
  const xpath= x_path
  const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
  const element = result.singleNodeValue;
  console.log(element)
  if (element) {
    element.addEventListener('click', function() {
      const pageLoadHandler = function() {
        window.removeEventListener('load', pageLoadHandler);
        // Do whatever you want to do once the page is loaded
        console.log('Page loaded!');
      };
      window.addEventListener('load', pageLoadHandler);
    });
    element.dispatchEvent(new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window
    }));
    return 'True'
  } else {
    console.error('No element found with selector!');
    return null;
  }
}

async function clickButtonByCssSelector(css_sel: any) {
  //console.log({css_sel})
  const elements = document.querySelectorAll(css_sel);
  console.log(elements)
  if (elements[0]) {
    elements[0].dispatchEvent(new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window
    }));
  } else {
    console.error('No element found with selector!');
  }
}

async function clickAds(xpath: any) {
  const elements = document.querySelectorAll(xpath);
  console.log(elements);

  for (let i = 0; i < elements.length; i++) {
    const parentElement = elements[i];
    const childElement = parentElement.querySelector('a.sVXRqc');
    if (!childElement) {
      console.log(`Child element with class 'sVXRqc' not found within parent element.`);
      continue;
    }
  
    const link = childElement.href;
    window.open(link, '_self');

    await new Promise(resolve => setTimeout(resolve, 5000)); 
    chrome.runtime.sendMessage({ action: 'performActionsOnTab' });
    console.log('button clicked')
    // window.history.back()
  }
}


function clickRandomAds(selector1: any, selector2: any) {
  const elements1 = document.querySelectorAll(selector1);
  const elements2 = document.querySelectorAll(selector2);

  const allElements = Array.from(elements1).concat(Array.from(elements2));

  const randomIndex = Math.floor(Math.random() * allElements.length);
  const parentElement = allElements[randomIndex];
  let childElement = parentElement.querySelector("a[style='display:none']");

  
  if (!childElement) {
    childElement = parentElement.querySelector("a.sVXRqc");
  }
  if (childElement) {
    const link = childElement.href;
    const newTab = window.open(link, '_self');
    //new Promise(resolve => setTimeout(resolve, 5000));
    return link; // Return the URL that was clicked
  } else {
    console.log(`Child element not found within parent element.`);
    return null; // Return null if no URL was clicked
  }
}

function clickRandomAds1(selector: any) {
  const element = document.querySelector(selector);

  if (!element) {
    console.log(`No element found with the given selector.`);
    return null;
  } else {
    // Click on the element
    element.click();
    return element.href; // Return the URL that was clicked
  }
}





function closeCurrentTab() {
  chrome.runtime.sendMessage({ action: 'CloseTab' });
}

function openURLInCurrentTab(url: any) {
  const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(url)}`;
  chrome.runtime.sendMessage({ action: 'OpenURLInCurrentTab', url: searchUrl });
}

function scrollDown(down: any) {
  window.scrollTo(0, window.scrollY + down);
}

function scrollUp(up: any) {
  window.scrollTo(0, window.scrollY - up);
}

function goBack() {
  window.history.back();
}

function doesElementExist(cssSelector: any) {
  const element = document.querySelector(cssSelector);
  return !!element; // Convert the element presence to true/false
}

function getInnerHTMLByTagName(id: any) {
  console.log('In tag funcation', );
  const element = document.getElementById(id);
  if (element) {
    console.log('element', element);
    return element.innerHTML;
  }
  return null; // Return null if the element is not found
}

function clearCookies() {
  const urlToClear = "https://sodataste.com"; // Replace with the URL you want to clear site data for
  chrome.runtime.sendMessage({ action: "clearAllSiteData" });
}



function refreshPage() {
  window.location.href = window.location.href;
}

chrome.runtime.onMessage.addListener(async (request: { action: string; data: { selector: any, selector2: any; } }, sender: any, sendResponse: any) => {
  console.log("listener");

  if (request.action === 'refreshPage') {
    refreshPage();
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'Page refreshed' });
  }

  if (request.action === 'clickButtonByXpath') {
    const element = await clickButtonByXpath(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: element }); 
  }

  if (request.action === 'clickButtonBySelector') {
    console.log({request})
    await clickButtonByCssSelector(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'Button clicked by CSS!' }); 
  }

  if (request.action === 'clickAds') {
   
    await clickAds(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'clicked on Ads'});
  }

  if (request.action === 'clickRandomAds') {
   
    const element = await clickRandomAds(request.data.selector,request.data.selector2);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: element});
  }

  if (request.action === 'clickRandomAds1') {
  
    const element = await clickRandomAds1(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: element});
  }


  if (request.action === 'closeTab') {
   
    closeCurrentTab();
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'clicked on Ads'});
  }

  if (request.action === 'openMainTab') {
   
    openURLInCurrentTab(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'Open base URL'});
  }
  if (request.action === 'scrollDown') {
    scrollDown(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'Scrolled down' });
  }

  if (request.action === 'scrollUp') {
    scrollUp(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'Scrolled up' });
  }
  if (request.action === 'goBack') {
    goBack();
    chrome.runtime.sendMessage({ action: 'sendMessage', message: 'Go Back' });
  }
  if (request.action === 'doesElementExist') {
    const results = doesElementExist(request.data.selector);
    chrome.runtime.sendMessage({ action: 'sendMessage', message: results });
  }
  if (request.action === 'clearCookies') {
    const results = clearCookies();
    chrome.runtime.sendMessage({ action: 'sendMessage', message: results });
  }
  


  // click button by css selector
  // click button by xpath
  // get html by css selector
  // get html by xpath  
});


function sleep(arg0: number) {
  throw new Error('Function not implemented.');
}

