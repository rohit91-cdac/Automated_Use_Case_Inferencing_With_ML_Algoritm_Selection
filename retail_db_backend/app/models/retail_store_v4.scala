package models

import play.api.libs.json.Json
import reactivemongo.api.bson.{BSONDocument, BSONDocumentReader, BSONDocumentWriter}

import scala.util.Try

case class retail_store_v4(
                          uri: String,
                          name: String,
                          sku: String,
                          selling_price : Float,
                          original_price: String,
                          currency: String,
                          availability: String,
                          color: String,
                          category: String,
                          source: String,
                          source_website: String,
                          breadcrumbs: String,
                          description: String,
                          brand: String,
                          images: String,
                          country:String,
                          language: String,
                          average_rating: Float,
                          review_count: Int,
                          crawled_at: String
                          )

object retail_store_v4 {

  implicit val retailStoreV4 = Json.format[retail_store_v4]

  implicit object retail_store_v4_reader extends BSONDocumentReader[retail_store_v4]  {
    override def readDocument(doc: BSONDocument): Try[retail_store_v4] = for {
      uri <- doc.getAsTry[String]("uri")
      name <- doc.getAsTry[String]("name")
      sku <- doc.getAsTry[String]("sku")
      selling_price <- doc.getAsTry[Float]("selling_price")
      original_price <- doc.getAsTry[String]("original_price")
      currency <- doc.getAsTry[String]("currency")
      availability <- doc.getAsTry[String]("availability")
      color <- doc.getAsTry[String]("color")
      category <- doc.getAsTry[String]("category")
      source <- doc.getAsTry[String]("source")
      source_website <- doc.getAsTry[String]("source_website")
      breadcrumbs <- doc.getAsTry[String]("breadcrumbs")
      description <- doc.getAsTry[String]("description")
      brand <- doc.getAsTry[String]("brand")
      images <- doc.getAsTry[String]("images")
      country <- doc.getAsTry[String]("country")
      language <- doc.getAsTry[String]("language")
      average_rating <- doc.getAsTry[Float]("average_rating")
      review_count <- doc.getAsTry[Int]("review_count")
      crawled_at <- doc.getAsTry[String]("crawled_at")
    } yield new retail_store_v4(uri = uri, name = name, sku = sku, selling_price = selling_price, original_price = original_price,
      currency = currency, availability = availability, color = color, category = category, source = source, source_website = source_website,
      breadcrumbs = breadcrumbs, description = description, brand = brand, images = images, country = country, language = language,
      average_rating = average_rating, review_count = review_count, crawled_at = crawled_at)
  }

  implicit object retail_store_v4_writer extends  BSONDocumentWriter[retail_store_v4] {

    override def writeTry(t: retail_store_v4): Try[BSONDocument] = Try {
      BSONDocument(
        "uri" -> t.uri,
        "name" -> t.name,
        "sku" -> t.sku,
        "selling_price" -> t.selling_price,
        "original_price" -> t.original_price,
        "currency" -> t.currency,
        "availability" -> t.availability,
        "color" -> t.color,
        "category" -> t.category,
        "source" -> t.source,
        "source_website" -> t.source_website,
        "breadcrumbs" -> t.breadcrumbs,
        "description" -> t.description,
        "brand" -> t.brand,
        "images" -> t.images,
        "country" -> t.country,
        "language" -> t.language,
        "average_rating" -> t.average_rating,
        "review_count" -> t.review_count,
        "crawled_at" -> t.crawled_at
      )
    }
  }
}
