name := """retail_db_backend"""
organization := "com.accenture"

version := "1.0-SNAPSHOT"

lazy val root = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.13.11"

libraryDependencies += guice
libraryDependencies += "org.scalatestplus.play" %% "scalatestplus-play" % "5.1.0" % Test
libraryDependencies += "org.reactivemongo" %% "play2-reactivemongo" % "1.1.0-play28-RC11"


// Adds additional packages into Twirl
//TwirlKeys.templateImports += "com.accenture.controllers._"

// Adds additional packages into conf/routes
// play.sbt.routes.RoutesKeys.routesImport += "com.accenture.binders._"
