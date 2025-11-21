package rabbit

import (
	"encoding/json"
	"log"
	"os"

	"worker-go/internal/models"

	amqp "github.com/rabbitmq/amqp091-go"
)

type MessageHandler func(data models.WeatherPayload) error

func Consume(conn *amqp.Connection, handler MessageHandler) error {
	ch, err := conn.Channel()
	if err != nil {
		return err
	}
	defer ch.Close()

	queueName := os.Getenv("RABBITMQ_QUEUE")

	// Garante que a fila existe antes de consumir (idempotente)
	_, err = ch.QueueDeclare(
		queueName,
		true,  // durable
		false, // auto-delete
		false, // exclusive
		false, // no-wait
		nil,
	)
	if err != nil {
		return err
	}

	// Inicia o consumo
	msgs, err := ch.Consume(
		queueName,
		"go-worker",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return err
	}

	log.Println("Go worker aguardando mensagens...")

	for msg := range msgs {
		var data models.WeatherPayload

		if err := json.Unmarshal(msg.Body, &data); err != nil {
			log.Println("Erro ao decodificar JSON:", err)
			msg.Nack(false, false)
			continue
		}

		if err := handler(data); err != nil {
			log.Println("Erro ao processar:", err)
			msg.Nack(false, true)
			continue
		}

		msg.Ack(false)
	}

	return nil
}
