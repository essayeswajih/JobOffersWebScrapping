import scrapy

class ExampleSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.offre-emploi.tn/",
    ]

    def parse(self, response):
        job_count = 0  # Counter to track how many jobs are scraped
        for article in response.xpath("//article"):
            job_count += 1
            
            # Safely handle missing descriptions
            description = article.css("div.preview::text").get()
            if description:
                description = description.strip()
            else:
                description = "Description not available"

            yield {
                "jobTitle": article.css("div.jobTitle h2 a span::text").get(),
                "category": article.css("div.location a:nth-child(1) span::text").get(),
                "location": article.css("div.location a:nth-child(2) span::text").get(),
                "description": description,
                "postedDate": article.css("div.postedDate time::attr(datetime)").get(),
            }
        
        self.log(f"Scraped {job_count} jobs from the current page.")

        # Find the "Suivant" (Next) page link
        next_page = response.css("div.pagingWrapper a:contains('Suivant')::attr(href)").get()
        
        if next_page:
            self.log(f'Following next page: {next_page}')
            yield response.follow(next_page, self.parse)
        else:
            self.log('No more pages to follow.')
