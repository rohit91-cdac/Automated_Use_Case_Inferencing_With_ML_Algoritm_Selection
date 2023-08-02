package controllers

import models.{retail_store_v1, retail_store_v2, retail_store_v3, retail_store_v4}
import play.api._
import play.api.libs.json.Format.GenericFormat
import play.api.libs.json.Json
import play.api.mvc._
import play.modules.reactivemongo._
import reactivemongo.api.bson.collection.{BSONCollection, BSONSerializationPack}
import reactivemongo.api.bson.{BSONDocument, BSONValue}
import reactivemongo.api.collections._
import reactivemongo.api.gridfs.{GridFS, ReadFile}
import reactivemongo.api.{AsyncDriver, MongoConnection}
import reactivemongo.play.json._

import javax.inject._
import scala.concurrent.duration.Duration
import scala.concurrent.{Await, ExecutionContext, Future}
import scala.util.{Failure, Success}

/**
 * This controller creates an `Action` to handle HTTP requests to the
 * application's home page.
 */
@Singleton
class HomeController @Inject()(override val controllerComponents: ControllerComponents,
                               val reactiveMongoApi: ReactiveMongoApi,
                               implicit val materialize: akka.stream.Materializer,
                              )(implicit ec: ExecutionContext) extends AbstractController(controllerComponents) with MongoController with ReactiveMongoComponents {

  /**
   * Create an Action to render an HTML page.
   *
   * The configuration in the `routes` file means that this method
   * will be called when the application receives a `GET` request with
   * a path of `/`.
   */

  val fsParser = gridFSBodyParser(reactiveMongoApi.asyncGridFS)
  val gfs: GridFS[BSONSerializationPack.type] = null
  val gridfs = reactiveMongoApi.asyncGridFS
  val driver_mongo = new AsyncDriver()
  val uri = "mongodb://localhost:27017/retailDB"
  val parsed_conn = Await.result(MongoConnection.fromString(uri = uri), atMost = Duration(10, "seconds"))
  val connection_local = Await.result(driver_mongo.connect(parsed_conn), atMost = Duration(10, "seconds"))
  def dbFromConnection(connection: MongoConnection, collection_name: String): Future[BSONCollection] =
    connection.database("retailDB").
      map(_.collection(collection_name))

  def upload() = Action(fsParser) { request =>
    // here is the future file!
    val file: ReadFile[BSONValue, BSONDocument] = request.body.files.head.ref
    val file_name = file.filename.get
    val file_length = request.body.files.head.ref.length

    // do something with `file`
    Ok(Json.obj("Name" -> file_name, "file_length" -> file_length))
  }

  def store_input_file() = Action.async(parse.multipartFormData) { request =>
    val multipart = request.body
    val file = multipart.file("retail_file").get.ref.file
    val key_file = multipart.dataParts.get("retail_file_type").get.head
    println(s"Received File for Key $key_file")
    val all_lines = scala.io.Source.fromFile(file).getLines.drop(1)
    val retail_class_list = key_file match {
      case "A_Store_Sale" => all_lines.map {
        each_line =>
          val split_line = each_line.split(',')
          retail_store_v1(
            store = Integer.parseInt(split_line(0)),
            sale_date = split_line(1),
            sale_weekly = split_line(2).toFloat,
            holiday_flag = Integer.parseInt(split_line(3)),
            temperature = split_line(4).toFloat,
            fuel_price = split_line(5).toFloat,
            cpi = split_line(6).toFloat,
            unemployment = split_line(7).toFloat
          )
      }.toList
      case "B_Store_Sale" => all_lines.map {
        each_line =>
          val split_line = each_line.split(',')
          retail_store_v2(
            ship_mode = split_line(0),
            segment = split_line(1),
            country = split_line(2),
            city = split_line(3),
            state = split_line(4),
            postal_code = split_line(5).toDouble,
            region = split_line(6),
            category = split_line(7),
            sub_category = split_line(8),
            sales = split_line(9).toFloat,
            quantity = Integer.parseInt(split_line(10)),
            discount = split_line(11).toFloat,
            profit = split_line(12).toFloat
          )
      }
      case "C_Store_Sale" => all_lines.map {
        each_line =>
          val split_line = each_line.split(',')
          retail_store_v3(
            invoice = Integer.parseInt(split_line(0)),
            stock_code = split_line(1),
            description = split_line(2),
            quantity = Integer.parseInt(split_line(3)),
            invoice_date = split_line(4),
            price = split_line(5).toFloat,
            customer_id = Integer.parseInt(split_line(6)),
            country = split_line(7)
          )
      }
      case "D_Store_Sale" => all_lines.map {
        each_line =>
          val split_line = each_line.split(',')
          retail_store_v4(
            uri = split_line(0),
            name = split_line(1),
            sku = split_line(2),
            selling_price = split_line(3).toFloat,
            original_price = split_line(4),
            currency = split_line(5),
            availability = split_line(6),
            color = split_line(7),
            category = split_line(8),
            source = split_line(9),
            source_website = split_line(10),
            breadcrumbs = split_line(11),
            description = split_line(12),
            brand = split_line(13),
            images = split_line(14),
            country = split_line(15),
            language = split_line(16),
            average_rating = split_line(17).toFloat,
            review_count = Integer.parseInt(split_line(18)),
            crawled_at = split_line(19)
          )
      }
      case _ => List[retail_store_v1]()
    }

    val insert_map = key_file match {
      case "A_Store_Sale" =>
        val bson_coll = Await.result(dbFromConnection(connection = connection_local, collection_name = "Retail_Store_One"), atMost = Duration(10, "seconds"))
        bson_coll.insert.many(retail_class_list.asInstanceOf[List[retail_store_v1]])
      case "B_Store_Sale" =>
        val bson_coll = Await.result(dbFromConnection(connection = connection_local, collection_name = "Retail_Store_Two"), atMost = Duration(10, "seconds"))
        bson_coll.insert.many(retail_class_list.asInstanceOf[List[retail_store_v2]])
      case "C_Store_Sale" =>
        val bson_coll = Await.result(dbFromConnection(connection = connection_local, collection_name = "Online_Store_One"), atMost = Duration(10, "seconds"))
        bson_coll.insert.many(retail_class_list.asInstanceOf[List[retail_store_v3]])
      case "D_Store_Sale" =>
        val bson_coll = Await.result(dbFromConnection(connection = connection_local, collection_name = "Online_Store_Two"), atMost = Duration(10, "seconds"))
        bson_coll.insert.many(retail_class_list.asInstanceOf[List[retail_store_v4]])
    }

    insert_map.onComplete{
      case Failure(e) => e.printStackTrace()
      case Success(_) => println(s"Successfully Inserted documents with result")
    }

//    val list_bson_document = list_retail_class.map{
//      each_case =>
//        println(s"Inserting Store ${each_case.store}")
//        BSONDocument(
//          "store" -> each_case.store,
//          "sale_date" -> each_case.sale_date,
//          "sale_weekly" -> each_case.sale_weekly,
//          "holiday_flag" -> each_case.holiday_flag,
//          "temperature" -> each_case.temperature,
//          "fuel_price" -> each_case.fuel_price,
//          "cpi" -> each_case.cpi,
//          "unemployment" -> each_case.unemployment
//        )
//    }
//    val insert_op_many = bson_coll.insert.many(list_retail_class)
//
//    insert_op_many.onComplete{
//      case Failure(e) => e.printStackTrace()
//      case Success(_) => println(s"Successfully Inserted documents with result")
//    }

    Future {
      Ok(Json.obj("Message" -> "Records have been inserted" ))
    }
  }
}
