import FileUpload from '../components/FileUpload';

//home page component
const Home = () => {
    return ( 
        <div className="home">
            {/* adding the file upload, which is the only component used on this page*/}
            <FileUpload/>
        </div>
     );
}
 
export default Home ;