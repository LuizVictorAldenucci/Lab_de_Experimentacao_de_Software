const { graphqlHTTP } = require("express-graphql")
const { buildSchema } = require("graphql")
const data = require("./dataset/data.json")

const schema = buildSchema(`
  type User {
    id: Int
    name: String
    email: String
  }

  type Query {
    user(id: Int!): User
    users: [User]
  }
`)

const root = {
  user: ({ id }) => data.users.find(u => u.id === id),
  users: () => data.users
}

module.exports = app => {
  app.use(
    "/graphql",
    graphqlHTTP({
      schema,
      rootValue: root,
      graphiql: false
    })
  )
}
