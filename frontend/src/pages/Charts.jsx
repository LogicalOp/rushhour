import ChartsList from '../components/ChartsList';
//charts page component
const Charts = () => {
    return ( 
        <div className="home">
        {/* adding the charts list, which is the only component used on this page*/}

            <ChartsList/>
            
            
        </div>
     );
}
 
export default Charts ;