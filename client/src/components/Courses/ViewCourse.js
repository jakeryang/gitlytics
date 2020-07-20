import React, { useEffect, useState } from 'react';
import { useParams, useHistory, Link } from 'react-router-dom';
import { Container, Grid, Typography, IconButton } from '@material-ui/core';
import { getCourse } from '../../api/courseService';
import { useLoader } from '../../LoadContext';
import AddIcon from '@material-ui/icons/Add'
import InviteUserDialog from '../Invites/InviteUserDialog';
import ProjectList from '../Projects/ProjectList';

export default function ViewCourse(){
    const {course_id} = useParams();
    const [data, setData] = useState({})
    const { state, dispatch } = useLoader()

    const [inviteDialogOpen, setInviteOpen] = useState(false)

    const history = useHistory()

    useEffect(() => {
        dispatch("LOADING")
        getCourse(course_id)
        .then(data => {
            setData(data)
            dispatch("FINISHED")
        })
        .catch(error => {
            history.push('/courses')
        })
    }, [])

    function goToCreateProject(e){
        history.push(`/courses/${course_id}/p/create`)
    }

    function addInvites(d){
        let cpy = {...data}
        cpy.invites = cpy.invites.concat(d.invites)
        setData(cpy)
    }

    function deleteProject(id){
        let cpy = {...data}
        cpy.course.projects = cpy.course.projects.filter(p => p.id !== id)
        setData(cpy)
    }

    return (
        <Container maxWidth="lg">
        {data.course !== undefined && (
            <Grid
                container
                direction="row"
                justify="flex-start"
                alignItems="flex-start"
            >
                <Grid item xs={12}>
                    <Typography variant="h3">
                        {data.course.name}
                    </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="h4">
                        Projects
                        {data.invites !== undefined && (
                            <IconButton onClick={goToCreateProject}>
                                <AddIcon />
                            </IconButton>
                        )}
                    </Typography>
                    {data.course.projects && <ProjectList projects={data.course.projects} deleteProject={deleteProject}/>}
                </Grid>
                <Grid item xs={6}>
                    <Typography variant="h4">
                        Students
                    </Typography>
                    {data.course.users.map(user => (
                        <Typography key={user.id}>
                            {user.username}
                        </Typography>
                    ))}
                    {data.course.users.length === 0 && (
                        <Typography>
                            No students
                        </Typography>
                    )}
                    {data.invites !== undefined && (
                        <div>
                            <Typography variant="h5">
                                Invited Students
                                    <IconButton onClick={() => setInviteOpen(true)}>
                                        <AddIcon/>
                                    </IconButton>
                            </Typography>
                            <InviteUserDialog open={inviteDialogOpen} setOpen={setInviteOpen} courseId={data.course.id} addInvites={addInvites}/>
                            <div>
                            {data.invites.length === 0 && (
                                <Typography>
                                    No invites
                                </Typography>
                            )}
                            </div>
                            <div>
                            {data.invites.map(invite => (
                                <Typography key={invite.id}>
                                    {invite.username}
                                </Typography>
                            ))}
                            </div>
                        </div>
                    )}
                </Grid>
            </Grid>
        
        )} 
        </Container>
    )
}