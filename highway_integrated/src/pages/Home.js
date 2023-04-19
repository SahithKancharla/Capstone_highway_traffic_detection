import '../styles/Home.css'


function Home(){
    return (
        <div className = "introduction-container">
            <div className = "head-text">
                <div className = "head-image">
                    <img src = {require ('../images/intersection.png')} alt = "Freedom Blog"  className = "main-img"/>
                </div>
                {/* <h3 className = 'text'> Escape traffic while you can </h3> */}
            </div>
            <div>
            </div>
        </div>
    );
}

export default Home;