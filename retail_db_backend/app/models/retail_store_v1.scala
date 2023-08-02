package models

import play.api.libs.json.Json
import reactivemongo.api.bson._

import scala.util.Try

case class retail_store_v1(
                          store: Int,
                          sale_date: String,
                          sale_weekly: Float,
                          holiday_flag: Int,
                          temperature: Float,
                          fuel_price: Float,
                          cpi: Float,
                          unemployment: Float
                          )

object retail_store_v1 {
  implicit val retailStoreV1 = Json.format[retail_store_v1]
  implicit object retail_store_v1_reader extends BSONDocumentReader[retail_store_v1] {
    override def readDocument(doc: BSONDocument): Try[retail_store_v1] = for {
      store <- doc.getAsTry[Int]("store")
      sale_date <- doc.getAsTry[String]("sale_date")
      sale_weekly <- doc.getAsTry[Float]("sale_weekly")
      holiday_flag <- doc.getAsTry[Int]("holiday_flag")
      temperature <- doc.getAsTry[Float]("temperature")
      fuel_price <- doc.getAsTry[Float]("fuel_price")
      cpi <- doc.getAsTry[Float]("cpi")
      unemployment <- doc.getAsTry[Float]("unemployment")
    } yield new retail_store_v1(
      store = store, sale_date = sale_date, sale_weekly = sale_weekly, holiday_flag = holiday_flag,
      temperature = temperature, fuel_price = fuel_price, cpi = cpi, unemployment = unemployment
    )
  }

  implicit object writeDocument extends BSONDocumentWriter[retail_store_v1] {
    override def writeTry(t: retail_store_v1): Try[BSONDocument] = Try {
      BSONDocument(
        "store" -> t.store,
        "sale_date" -> t.sale_date,
        "sale_weekly" -> t.sale_weekly,
        "holiday_flag" -> t.holiday_flag,
        "temperature" -> t.temperature,
        "fuel_price" -> t.fuel_price,
        "cpi" -> t.cpi,
        "unemployment" -> t.unemployment
      )
    }
  }
}
