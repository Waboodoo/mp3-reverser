const API_BASE_PATH = '/api'
const POLL_ITERATION_LIMIT = 25;

function sleep(ms: number): Promise<any> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getPollDelay(iteration: number): number {
    if (iteration < 3) {
        return 500;
    }
    if (iteration < 6) {
        return 1500;
    }
    return 3000;
}

interface ProcessResult {
    url: string;
}

interface Options {
    reverse: boolean;
    speed: number;
    keepPitch: boolean;
    stereoShift: boolean;
}

class APIClient {
    async upload(file: File, options: Options): Promise<ProcessResult> {
        const formData = new FormData();
        formData.append('file', file);
        for (const [key, value] of Object.entries(options)) {
            formData.append(key, value);
        }
        const response = await fetch(`${API_BASE_PATH}/process`, {
            method: 'POST',
            body: formData,
        });
        const responseData = await response.json();
        const statusUrl = responseData.status_url;

        for (let iteration = 0; iteration < POLL_ITERATION_LIMIT; iteration++) {
            await sleep(getPollDelay(iteration));
            const statusResponse = await fetch(statusUrl);
            const statusData = await statusResponse.json()
            if (statusData.status === 'done') {
                return {
                    url: statusData.result_url,
                };
            }
            if (statusData.status === 'error') {
                throw Error('Backend failed to process request');
            }
        }
        throw Error('Backend took too long to process request');
    }
}

export default APIClient;
