const express = require("express")
const data = require("./dataset/data.json")

const router = express.Router()

router.get("/user/:id", (req, res) => {
  const user = data.users.find(u => u.id == req.params.id)
  res.json({ user })
})

router.get("/users", (req, res) => {
  res.json({ users: data.users })
})

module.exports = router
