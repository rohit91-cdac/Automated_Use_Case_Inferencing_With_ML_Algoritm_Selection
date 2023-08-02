package models

import play.api.libs.json.Json
import reactivemongo.api.bson.{BSONDocument, BSONDocumentReader, BSONDocumentWriter}

import scala.util.Try

case class retail_store_v3(
                          invoice: Int,
                          stock_code: String,
                          description: String,
                          quantity: Int,
                          invoice_date: String,
                          price: Float,
                          customer_id: Int,
                          country: String
                          )

object retail_store_v3 {
  implicit val retailStoreV3 = Json.format[retail_store_v3]

  implicit object retail_store_v3_reader extends BSONDocumentReader[retail_store_v3] {

    override def readDocument(doc: BSONDocument): Try[retail_store_v3] = for {
      invoice <- doc.getAsTry[Int]("invoice")
      stock_code <- doc.getAsTry[String]("stock_code")
      description <- doc.getAsTry[String]("description")
      quantity <- doc.getAsTry[Int]("quantity")
      invoice_date <- doc.getAsTry[String]("invoice_date")
      price <- doc.getAsTry[Float]("price")
      customer_id <- doc.getAsTry[Int]("customer_id")
      country <- doc.getAsTry[String]("country")
    } yield new retail_store_v3(invoice = invoice, stock_code = stock_code, description = description, quantity = quantity,
      invoice_date = invoice_date, price = price, customer_id = customer_id, country = country)
  }

  implicit object retail_store_v3_writer extends BSONDocumentWriter[retail_store_v3] {

    override def writeTry(t: retail_store_v3): Try[BSONDocument] = Try {
      BSONDocument(
        "invoice" -> t.invoice,
        "stock_code" -> t.stock_code,
        "description" -> t.description,
        "quantity" -> t.quantity,
        "invoice_date" -> t.invoice_date,
        "price" -> t.price,
        "customer_id" -> t.customer_id,
        "country" -> t.country
      )
    }
  }
}
