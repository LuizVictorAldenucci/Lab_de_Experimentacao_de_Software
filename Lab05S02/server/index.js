const express = require("express")
const rest = require("./rest")
const graphql = require("./graphql")

const app = express()
app.use(express.json())

// REST
app.use("/api", rest)

// GraphQL
graphql(app)

app.listen(4000, () => {
  console.log("API running on http://localhost:4000")
})
