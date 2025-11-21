package httpclient

import (
	"bytes"
	"encoding/json"
	"net/http"
)

func PostJSON(url string, body any) (*http.Response, error) {
	jsonData, _ := json.Marshal(body)
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	return client.Do(req)
}
