
import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { SWRConfig } from 'swr';
import axios from 'axios';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SWRConfig 
      value={{
        fetcher: (url: string) => axios.get(url).then(res => res.data),
        revalidateOnFocus: false
      }}
    >
      <Component {...pageProps} />
    </SWRConfig>
  );
}

export default MyApp;
