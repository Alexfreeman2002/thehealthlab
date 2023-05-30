// api reference: https://gnews.io/docs/v4?javascript#top-headlines-query-parameters

var apikey = 'c85d9b57e2349444885af3a5da2ad676';
var category = 'health';
var url = 'https://gnews.io/api/v4/top-headlines?category=' + category + '&lang=en&country=us&max=10&apikey=' + apikey;

// Initiates a network request to the specified URL
fetch(url)
  .then(function (response) {
    // Parses the response as JSON and returns a Promise
    return response.json();
  })
  .then(function (data) {
    // Retrieves the 'articles' array from the response data
    var articles = data.articles;
    // Variable to store the generated HTML for news items
    var newsHTML = '';

    // Loop through each article in the 'articles' array
    for (var i = 0; i < articles.length; i++) {
      // Get the current article
      var article = articles[i];
      // Log the title of the article
      console.log("Title: " + article.title);
      // Log the description of the article
      console.log("Description: " + article.description);
      // Log the published date of the article
      console.log("Published At: " + articles[i]['publishedAt']);

      // Generate HTML for a news item and append it to the 'newsHTML' string
      newsHTML += '<div class="news-item">';
      newsHTML += '<h2>' + article.title + '</h2>';
      newsHTML += '<p>' + article.description + '</p>';
      newsHTML += '</div>';
    }

    // Get the element with the ID 'news-container'
    var newsContainer = document.getElementById('news-container');
    // Set the generated HTML as the content of the 'newsContainer' element
    newsContainer.innerHTML = newsHTML;
  });






