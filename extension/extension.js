// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

const legend = new vscode.SemanticTokensLegend(
	[reserved, constant, operator, sepertor, string, space, cpmment, error, assigner, variable, function, package],
	[]
);

class MyDocumentSemanticTokensProvider {
	constructor() {
		// nothing to do
	}

	provideDocumentSemanticTokens(document) {
		// run python code for lexical, syntactic, semantic analysis
		// (assume this extention.js is at . )
		// run ./analyzer/main.py
		// it will generate a colors.pyknights file
		// read that file as an array of dicts
		// reinterpret that array to become the data part of SemanticTokens
		// return that SemanticTokens

		// 1. run python code at ./analyzer/main.py
		const { spawn } = require('child_process');
		const python = spawn('python', ['./analyzer/main.py', '--file', document.fileName]);

		// 2. read from ./analyzer/colors.pyknights
		const fs = require('fs');
		const path = require('path');
		const filepath = path.join(__dirname, './analyzer/colors.pyknights');
		const colors = JSON.parse(fs.readFileSync(filepath, 'utf8'));

		// 3. reinterpret colors to become the data part of SemanticTokens
		const builder = new vscode.SemanticTokensBuilder();
		for (const item of colors) {
			builder.push(
				item.startLine - 1,
				item.startColumn - 1,
				item.endColumn - item.startColumn + 1,
				item.tokenType,
				[]
			);
		}

		// 4. return that SemanticTokens
		return builder.build();
	}

	provideDocumentRangeSemanticTokens(document, range) {
		// todo: run python code for lexical, syntactic, semantic analysis
	}
}

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This row of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "pyknights" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('pyknights.helloWorld', function () {
		// The code you place here will be executed every time your command is executed

		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from PyKnights!');
	});

	context.subscriptions.push(disposable);

	context.subscriptions.push(vscode.languages.registerDocumentSemanticTokensProvider(
		{ language: 'python' },
		new MyDocumentSemanticTokensProvider(),
		legend
	));

	vscode.workspace.onDidChangeTextDocument(event => {
        if (event.document.languageId === 'python') {
            console.log('Python code has been edited!');
			// todo: run python code for lexical, syntactic, semantic analysis
        }
    }, null, context.subscriptions);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate,
	MyDocumentSemanticTokensProvider
}
