package rabbit

import (
	"log"
	"os"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func Connect() (*amqp.Connection, error) {
	url := os.Getenv("RABBITMQ_URL")

	var conn *amqp.Connection
	var err error

	for {
		conn, err = amqp.Dial(url)
		if err == nil {
			log.Println("Conectado ao RabbitMQ!")
			return conn, nil
		}

		log.Println("RabbitMQ indisponível, tentando novamente em 2s...")
		time.Sleep(2 * time.Second)
	}
}
