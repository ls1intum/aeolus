import React, {useEffect, useRef, useState} from 'react';
import {Editor} from "@monaco-editor/react";
import {configureMonacoYaml} from "monaco-yaml";
import {Grid, Title, useComputedColorScheme} from "@mantine/core";
import {CodeHighlightTabs} from "@mantine/code-highlight";
import BashIcon from "../icons/BashIcon";
import BambooIcon from "../icons/BambooIcon";
import JenkinsIcon from "../icons/JenkinsIcon";

interface PlaygroundProps {
}

function Playground(props: PlaygroundProps) {
    window.MonacoEnvironment = {
        getWorker(moduleId, label) {
            switch (label) {
                case 'editorWorkerService':
                    return new Worker(new URL('monaco-editor/esm/vs/editor/editor.worker', import.meta.url))
                case 'json':
                    return new Worker(
                        new URL('monaco-editor/esm/vs/language/json/json.worker', import.meta.url)
                    )
                case 'yaml':
                    return new Worker(new URL('monaco-yaml/yaml.worker?worker', import.meta.url))
                default:
                    throw new Error(`Unknown label ${label}`)
            }
        }
    }
    let default_windfile: string = `api: v0.0.1
metadata:
  name: example windfile
  id: example-windfile
  description: This is a windfile with an internal action
  author: Andreas Resch
  docker:
    image: ls1tum/artemis-maven-template
    tag: java17-20
    volumes:
      - $\{WORKDIR}:/aeolus
    parameters:
      - --cpus
      - '"2"'
      - --memory
      - '"2g"'
      - --memory-swap
      - '"2g"'
      - --pids-limit
      - '"1000"'
  gitCredentials: artemis_gitlab_admin_credentials
repositories:
  aeolus:
    url: https://github.com/ls1intum/Aeolus.git
    branch: develop
    path: aeolus
actions:
  set-java-container:
    script: set
  set-c-container:
    docker:
      image: ghcr.io/ls1intum/artemis-c-docker
    script: set
  internal-action:
    script: |
      echo "This is an internal action"
  clean_up:
    script: |
      rm -rf aeolus/
    run_always: true`;
    const [data, setData] = useState<string>(default_windfile);
    const [markers, setMarkers] = useState<any[]>([]);

    const monacoRef = useRef<any>(null);

    function handleEditorWillMount(monaco: any) {
        configureMonacoYaml(monaco, {
            enableSchemaRequest: true,
            schemas: [
                {
                    fileMatch: ['**'],
                    uri: 'https://raw.githubusercontent.com/ls1intum/Aeolus/develop/schemas/v0.0.1/schemas/windfile.json'
                },
            ]
        });
    }

    function handleEditorDidMount(editor: any, monaco: any) {
        // here is another way to get monaco instance
        // you can also store it in `useRef` for further usage
        monacoRef.current = monaco;
    }

    const computedColorScheme = useComputedColorScheme('light', {getInitialValueInEffect: true});
    const editorTheme: 'vs-dark' | 'light' = computedColorScheme === 'dark' ? 'vs-dark' : 'light';

    const bashIcon = <BashIcon size={24}/>;
    const bambooIcon = <BambooIcon size={24}/>;
    const jenkinsIcon = <JenkinsIcon size={24}/>;

    const [target, setTarget] = React.useState<"cli" | "jenkins" | "bamboo">('cli');
    const [input, setInput] = React.useState<string>(default_windfile);

    const host = process.env.NODE_ENV === 'production' ? '/api' : 'http://127.0.0.1:8000';

    useEffect(() => {
        if (markers.length > 0) {
            return;
        }

        fetch(host + '/generate/' + target + '/yaml', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-yaml'
            },
            body: input,
        })
            .then(response => response.json())
            .catch(error => console.error('Error:', error))
            .then(data => data ? setData(data.result) : setData(''));
    }, [target, input, markers.length, host]);


    function handleEditorChange(value: string | undefined, _: any) {
        if (value === undefined) {
            setInput(default_windfile);
        } else {
            setInput(value);
        }
    }

    function handleValidate(markers: any[]) {
        setMarkers(markers);
    }

    const codeTabs: any[] = [
        {
            fileName: 'generated.sh',
            code: data ? data : 'enter a valid windfile to generate bash script',
            language: 'bash',
            icon: bashIcon,
        },
        {
            fileName: 'Bamboo Build Plan',
            code: data ? data : 'enter a valid windfile to generate Bamboo Build Plan',
            language: 'yaml',
            icon: bambooIcon,
        },
        {
            fileName: 'Jenkinsfile',
            code: data ? data : 'enter a valid windfile to generate Jenkinsfile',
            language: 'groovy',
            icon: jenkinsIcon,
        },
    ];

    return (
        <Grid gutter="md">
            <Grid.Col span={{base: 12, md: 6, lg: 6}}>
                <Title style={{
                    margin: '4px',
                }} order={4}>Define your job in aeolus:</Title>
                <Editor height="82vh" defaultLanguage="yaml" path="windfile.yaml" defaultPath="windfile.yaml"
                        defaultValue={default_windfile} theme={editorTheme} beforeMount={handleEditorWillMount}
                        onMount={handleEditorDidMount} onChange={handleEditorChange} onValidate={handleValidate}/>
            </Grid.Col>
            <Grid.Col span={{base: 12, md: 6, lg: 6}}>
                <Title style={{
                    margin: '4px',
                }} order={4}>...and watch what aeolus would generate:</Title>
                <CodeHighlightTabs
                    onTabChange={(tab) => {
                        const filename: string = codeTabs[tab].fileName;
                        if (filename === 'generated.sh') setTarget('cli');
                        else if (filename === 'Bamboo Build Plan') setTarget('bamboo');
                        else if (filename === 'Jenkinsfile') setTarget('jenkins');
                    }}
                    withExpandButton
                    defaultExpanded={false}
                    maxCollapsedHeight="78.25vh"
                    code={codeTabs}
                >
                </CodeHighlightTabs>
            </Grid.Col>
        </Grid>
    );
}

export default Playground;
