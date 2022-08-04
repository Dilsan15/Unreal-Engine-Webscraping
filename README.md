<h2>Summary</h2>
<p>Navigates a specific category of Unreal Engine forums, and retrieves text from all of the topics in that category. Uses BS4 and Selenium, among other libraries. Open source and free to use by anyone! </p>

<h2>Purpose</h2>
<p>Developed to help gather data for a ML internship project done in summer of 2022</p>


<h2>Processes</h2>

<ol>
  <li>Starts in a category link provided by user. Scrolls down and starts collecting links for topics in that category.</li>
  <li>Sets URL to one of the links collected (in order)</li>
  <li>Gets all text and Metadata from the page it enters</li>
  <li>Saves text data retrieved, a inserts it into a CSV file</li>
  <li>Continues process</li>
</ol>

<h2>Files</h2>

<ul>
  <li>Main: Defines variables which control output and runs connector </li>
  <li>connector: Connects wordscraper and form navigator together, allowing for data to be exchanged</li>
  <li>form_nav: Navigates forms, gets links to progress onto form page, sends HTML and metadata to wordscraper </li>
  <li>word_scraper: Parses HTML and gets all text from post and its replies. Saves Metadata and HTML to a CSV file</li>
  <li>form_data_collected: Contains all CSV file data from the forms scraped</li>
</ul>

<h2>Versions</h2>

<ul>
  <li>Python: 3.10.5</li>
  <li>BS4: 4.11.1 </li>
  <li>Selenium: 4.3.0</li>
<ul>


