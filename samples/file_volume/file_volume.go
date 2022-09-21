package main

import (
	"bufio"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"github.com/kittycad/kittycad.go"
	"io/ioutil"
	"os"
	"os/exec"
	"strings"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// KITTYCAD_API_TOKEN.
	client, _ := kittycad.NewClientFromEnv("your apps user agent")

	input, _ := os.Open("./ORIGINALVOXEL-3.obj")

	content, _ := ioutil.ReadAll(bufio.NewReader(input))

	// Encode as base64.
	myReader := strings.NewReader(base64.StdEncoding.EncodeToString(content))
	// LITTERBOX-END-NON-EDITABLE-SECTION

	fc, _ := client.File.CreateVolume(
		"obj",
		myReader,
	)

	fmt.Println("File volume: ", fc.Volume)

	json_data, _ := json.Marshal(struct {
		Title  string  `json:"title"`
		Volume float64 `json:"volume"`
	}{
		Title:  "output.json",
		Volume: fc.Volume,
	})

	// LITTERBOX-START-NON-EDITABLE-SECTION
	output_file_path := "./output.json"
	output, _ := os.Create(output_file_path)
	defer output.Close()
	output.Write(json_data)
	if err := output.Sync(); err != nil {
		panic(err)
	}
	exec.Command("cp", "./ORIGINALVOXEL-3.obj", "./output.obj").Output()
}
