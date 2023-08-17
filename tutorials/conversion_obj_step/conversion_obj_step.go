package main

import (
	"encoding/base64"
	"fmt"
	"os"

	"github.com/kittycad/kittycad.go"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// KITTYCAD_API_TOKEN.
	client, err := kittycad.NewClientFromEnv("your apps user agent")
	if err != nil {
		panic(err)
	}

	fileBytes, _ := os.ReadFile("./ORIGINALVOXEL-3.obj")

	fc, err := client.File.CreateConversion(kittycad.FileExportFormatStep, kittycad.FileImportFormatObj, fileBytes)
	if err != nil {
		panic(err)
	}

	fmt.Println("File conversion id: ", fc.ID)
	fmt.Println("File conversion status: ", fc.Status)

	decoded, err := base64.StdEncoding.DecodeString(fc.Output.String())
	if err != nil {
		panic(err)
	}

	output_file_path := "./output.step"
	fmt.Println("Saving output to ", output_file_path)

	output, err := os.Create(output_file_path)
	if err != nil {
		panic(err)
	}
	defer output.Close()

	if _, err := output.Write(decoded); err != nil {
		panic(err)
	}
	if err := output.Sync(); err != nil {
		panic(err)
	}
}
