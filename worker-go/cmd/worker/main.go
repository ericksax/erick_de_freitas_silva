package main

import (
	"log"

	"github.com/joho/godotenv"
	"your-module/internal/httpclient"
	"your-module/internal/models"
	"your-module/internal/rabbit"
)

func main() {
	godotenv.Load()

	conn, err := rabbit.Connect()
	if err != nil {
		log.Fatal("Erro ao conectar Rabbit:", err)
	}
	defer conn.Close()

	err = rabbit.Consume(conn, func(data models.WeatherPayload) error {
		return httpclient.SendWeatherData(data)
	})

	if err != nil {
		log.Fatal("Erro no consumer:", err)
	}
}
