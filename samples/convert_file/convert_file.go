package main

import (
	"fmt"
	"os"

	"github.com/kittycad/kittycad.go"
)

func main() {
	// Create a new client with your token parsed from the environment variable:
	// ZOO_API_TOKEN.
	client, err := kittycad.NewClientFromEnv("your apps user agent")
	if err != nil {
		panic(err)
	}

	fileBytes, _ := os.ReadFile("./ORIGINALVOXEL-3.obj")
	// LITTERBOX-END-NON-EDITABLE-SECTION

	fc, err := client.File.CreateConversion(
		kittycad.FileExportFormatStl,
		kittycad.FileImportFormatObj,
		fileBytes)
	if err != nil {
		panic(err)
	}

	fmt.Println("File conversion id: ", fc.ID)
	fmt.Println("File conversion status: ", fc.Status)

	// LITTERBOX-START-NON-EDITABLE-SECTION
	output_file_path := "./output.stl"
	fmt.Println("Saving output to ", output_file_path)

	output, err := os.Create(output_file_path)
	if err != nil {
		panic(err)
	}
	defer output.Close()

	if len(fc.Outputs) != 1 {
		panic("Expected 1 output file")
	}

	for _, contents := range fc.Outputs {
		if _, err := output.Write(contents.Inner); err != nil {
			panic(err)
		}
	}

	if err := output.Sync(); err != nil {
		panic(err)
	}
}
