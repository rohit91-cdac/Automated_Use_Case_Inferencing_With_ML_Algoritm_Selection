package models

import play.api.libs.json.Json
import reactivemongo.api.bson._

import scala.util.Try

case class retail_store_v2(
                          ship_mode: String,
                          segment: String,
                          country: String,
                          city: String,
                          state: String,
                          postal_code: Double,
                          region: String,
                          category: String,
                          sub_category: String,
                          sales: Float,
                          quantity: Int,
                          discount: Float,
                          profit: Float
                          )

object retail_store_v2 {
  implicit val retailStoreV2 = Json.format[retail_store_v2]
  implicit object retail_store_v2_reader extends BSONDocumentReader[retail_store_v2] {
    override def readDocument(doc: BSONDocument): Try[retail_store_v2] = for {
      ship_mode <- doc.getAsTry[String]("ship_mode")
      segment <- doc.getAsTry[String]("segment")
      country <- doc.getAsTry[String]("country")
      city <- doc.getAsTry[String]("city")
      state <- doc.getAsTry[String]("state")
      postal_code <- doc.getAsTry[Double]("postal_code")
      region <- doc.getAsTry[String]("region")
      category <- doc.getAsTry[String]("category")
      sub_category <- doc.getAsTry[String]("sub_category")
      sales <- doc.getAsTry[Float]("sales")
      quantity <- doc.getAsTry[Int]("quantity")
      discount <- doc.getAsTry[Float]("discount")
      profit <- doc.getAsTry[Float]("profit")
    } yield new retail_store_v2(ship_mode = ship_mode, segment = segment, country = country, city = city, state = state,
      postal_code = postal_code, region = region, category = category, sub_category = sub_category, sales = sales, quantity = quantity, discount = discount, profit = profit)
  }
  implicit object writeDocument extends  BSONDocumentWriter[retail_store_v2] {

    override def writeTry(t: retail_store_v2): Try[BSONDocument] = Try {
      BSONDocument(
        "ship_mode" -> t.ship_mode,
        "segment" -> t.segment,
        "country" -> t.country,
        "city" -> t.city,
        "state" -> t.state,
        "postal_code" -> t.postal_code,
        "region" -> t.region,
        "category" -> t.category,
        "sub_category" -> t.sub_category,
        "sales" -> t.sales,
        "quantity" -> t.quantity,
        "discount" -> t.discount,
        "profit" ->t.profit
      )
    }
  }
}
